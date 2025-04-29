from rest_framework import serializers
from .models import Car, Customer, Booking
from django.core.exceptions import ValidationError

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        car = data['car']
        start = data['start_date']
        end = data['end_date']
        booking_id = self.instance.id if self.instance else None

        overlapping = Booking.objects.filter(
            car=car,
            end_date__gte=start,
            start_date__lte=end
        ).exclude(id=booking_id)

        if overlapping.exists(): #checking if exist or not
            raise serializers.ValidationError("This car is already booked in the selected range.")
        return data
