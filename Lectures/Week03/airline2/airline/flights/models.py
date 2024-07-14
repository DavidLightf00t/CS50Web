from django.db import models

# Create your models here.
# AFTER EVERY NEW CLASS(MODEL) MUST MAKEMIGRATIONS THEN MIGRATE
# Airport Class to give to airport that the flights would be arriving and landing at
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

# Flight Class to add and remove flights from various locations and with various durations
class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    # Gives the Flight object a name
    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
    
# Passenger Class to create passengers and assign them to flights
class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    # Creates a variable that allows a passenger to have a 0, 1, or many flights allows access to see what passengers are on a given flight
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    # Returns the name of the passenger
    def __str__(self):
        return f"{self.first} {self.last}"

    

