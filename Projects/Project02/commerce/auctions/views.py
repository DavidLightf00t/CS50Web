from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Bids, Comments


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Listings.objects.all()
    })


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

        if not email:
            return render(request, "auctions/register.html", {
                "message": "Must Attatch an Email Account"
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        
        if not password:
            return render(request, "auctions/register.html", {
                "message": "Must Input a Password"
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

        if category and url:
            new_listing = Listings(title=title, description=description, photo=url, category=category, starting_bid=starting_bid)
            new_listing.save()
        
        if not url:
            new_listing = Listings(title=title, description=description, category=category, starting_bid=starting_bid)
            new_listing.save()
        
        if not category:
            new_listing = Listings(title=title, description=description, photo=url, starting_bid=starting_bid)
            new_listing.save()

        
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "auctions/newListing.html")
    

def listing(request, title):

    #Returns all of the info of the listing model. Title, Description, Photo Url, Category, and Starting Bid
    return render(request, "auctions/auctions.html", {
        "info": Listings.objects.get(title=title),
    })

def new_bid(request):
    if request.method == "POST":
        title = request.POST["title"]
        new_bid = request.POST["bid"]
        current_bid = Listings.objects.get(title=title)

        # We need to make the new bid into a float (originally a string)
        # We then need to compare the new bid passed to the current bid
        # If the new bid is greater update if not error
        new_bid = float(new_bid)
        
        if new_bid <= current_bid.starting_bid:
            return render(request, "auctions/auctions.html", {
                "info": Listings.objects.get(title=title),
                "message": "New Bid MUST be larger than current bid"
            })
        
        if User.is_authenticated == True:
            #Now that all of the bid info has been gotten, make a bid object
            Bids(new_bid, User.username, title)

            #TODO Make User info model work

            #Assign and save new bid
            current_bid.starting_bid = new_bid
            current_bid.save()

            #Update number of bids
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "auctions/login.html", {
                "message": "Must Be Logged In to Place Bids"
            })
    
    return render(request, "auctions/auctions.html", {
        "info": Listings.objects.get(title=title)
    })