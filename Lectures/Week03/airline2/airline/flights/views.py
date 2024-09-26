from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

#From models.py import the flight class(model)
from .models import Flight, Passenger

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        #Giving index.html access to an variable called flights that has access to all of the objects in the flights class
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    #Assigns flight ids to the flight variable
    flight = Flight.objects.get(id=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        # The reason flight.PASSENGERS.all() works is because the related name in models.py is "passengers"
        "non_passengers": Passenger.objects.exclude(flights=flight).all(),
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        # "passenger" is the input field named or form named passenger
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)

        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))