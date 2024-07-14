from django.urls import path

from . import views

urlpatterns = [
    #After each new pattern is created you need to go into views.py to make a new function for that path
    path("", views.index, name="index"),
    path("<int:flight_id>", views.flight, name="flight"),
    path("<int:flight_id>/book", views.book, name="book"),
]