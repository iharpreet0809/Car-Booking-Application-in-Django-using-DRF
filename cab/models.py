from django.db import models

# Create your models here.


class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.car} booked by {self.customer}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date.")

        overlapping = Booking.objects.filter(
            car=self.car,
            end_date__gte=self.start_date,
            start_date__lte=self.end_date
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError("This car is already booked for the selected date range.")
