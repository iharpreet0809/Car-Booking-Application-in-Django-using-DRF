from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics
from .models import Car, Customer, Booking
from .serializers import CarSerializer, CustomerSerializer, BookingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

@api_view(['GET'])
def available_cars(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date or not end_date:
        return Response({"error": "Please provide start_date and end_date"}, status=400)

    booked_cars = Booking.objects.filter(
        end_date__gte=start_date,
        start_date__lte=end_date
    ).values_list('car_id', flat=True)

    available = Car.objects.exclude(id__in=booked_cars).filter(available=True)
    serializer = CarSerializer(available, many=True)
    return Response(serializer.data)




#For the home page
def home(request):
    context = {
        'title': 'Home - Cab Booking',
        'message': 'Welcome to the Cab Booking System!',
    }
    return render(request, 'index.html', context)
