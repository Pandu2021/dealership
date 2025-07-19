# djangoapp/models.py
from django.db import models
from django.utils import timezone

# <HINT> Create a Car Make model
# CarMake has a name and description
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE) # Foreign key to CarMake
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('SPORTS', 'Sports Car'),
        ('HATCHBACK', 'Hatchback'),
        ('MINIVAN', 'Minivan'),
        ('TRUCK', 'Truck'),
        ('VAN', 'Van'),
        ('OTHER', 'Other')
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(default=2023, 
                               choices=[(r,r) for r in range(1900, timezone.now().year + 1)]) # Year field

    def __str__(self):
        return f"{self.car_make.name} - {self.name} ({self.year})"