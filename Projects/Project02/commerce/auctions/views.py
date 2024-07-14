from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


def index(request):
    return render(request, "auctions/index.html")

def newListing(request):
    return render(request, "auctions/newListing.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def newListing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        url = request.POST["url"]
        category = request.POST["category"]
        starting_bid = request.POST["starting_bid"]

        if not title:
            return render(request, "auctions/newListing.html", {
        "message": "Title Needed"
        })

        if not description:
            return render(request, "auctions/newListing.html", {
        "message": "Description Needed"
        })

        if not url and not category:
            return render(request, "auctions/newListing.html", {
        "message": "Url and/or Category Needed"
        })

        if not starting_bid:
            return render(request, "auctions/newListing.html", {
        "message": "Starting Bid Needed"
        })

        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "auctions/newListing.html")
