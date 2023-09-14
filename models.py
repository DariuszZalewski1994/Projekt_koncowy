from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Airport(models.Model):
    name = models.CharField(max_length=64)
    icao_code = models.CharField(max_length=4)
    runway_length = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.00)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, default=0.00)
    fuel_availability = models.BooleanField(default=False)

class Aircraft(models.Model):
    name = models.CharField(max_length=64)
    flight_range = models.IntegerField()
    takeoff_runway_length_required = models.IntegerField()
    landing_runway_length_required = models.IntegerField()

class FlightType(models.Model):
    name = models.CharField(max_length=64)

# class FuelAvailability(models.Model):
#     availability = models.BooleanField(default=False)
#     airport = models.OneToOneField(Airport, on_delete=models.CASCADE)

class Services(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    airport = models.ManyToManyField(Airport, blank=True)

class Flight(models.Model):
    flight_number = models.CharField(max_length=20, unique=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    flight_type = models.ForeignKey(FlightType, on_delete=models.CASCADE)
    departure_airport = models.ForeignKey(Airport, related_name='departure', on_delete=models.CASCADE)
    arrival_airport = models.ForeignKey(Airport, related_name='arrival', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)