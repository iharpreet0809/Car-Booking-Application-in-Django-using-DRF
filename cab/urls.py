from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, CarViewSet, CustomerViewSet, BookingViewSet, available_cars

router = DefaultRouter()
router.register('cars', CarViewSet)
router.register('customers', CustomerViewSet)
router.register('bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('available-cars/', available_cars),
]
