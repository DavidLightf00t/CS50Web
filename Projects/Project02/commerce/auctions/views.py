from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from sqlite3 import OperationalError

from .models import User, Listings, Bids, Comments, Watchlist


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

    try:
        bid_info = Bids.objects.filter(item=title).latest('id')

        #Returns all of the info of the listing model. Title, Description, Photo Url, Category, and Starting Bid
        return render(request, "auctions/auctions.html", {
            "listing_info": Listings.objects.get(title=title),
            "bid_info": bid_info
        })
    except ObjectDoesNotExist:
        bid_info = None
        
        return render(request, "auctions/auctions.html", {
                "listing_info": Listings.objects.get(title=title),
                "bid_info": bid_info
            })

def new_bid(request):
    if request.method == "POST":
        title = request.POST["title"]
        new_bid = request.POST["bid"]
        current_bid = Listings.objects.get(title=title)

        # We need to make the new bid into a float (originally a string)
        new_bid = float(new_bid)

        #Get User objects
        user = request.user.get_username()
        print(user)

        if user is not "":
            # We then need to compare the new bid passed to the current bid
            # If the new bid is greater update if not error
            if new_bid <= current_bid.starting_bid:
                return render(request, "auctions/auctions.html", {
                    "info": Listings.objects.get(title=title),
                    "message": "New Bid MUST be larger than current bid"
                })

            #Now that all of the bid info has been gotten, make a bid object then save it
            bid_object = Bids(bid_amount=new_bid, name=user, item=title)
            bid_object.save()

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


def category_view(request):
    # Make a new list of all of the non repeating categories
    category_list = []
    for objects in Listings.objects.all():
        # if object in category_list:
        if objects.category not in category_list:
            category_list.append(objects.category)

    return render(request, "auctions/category.html", {
        "info": category_list,
    })

def watchlist(request):
    print(request.method == "POST")

    if request.method == "POST":
        title = request.POST["title"]

        print("Going into POST", Watchlist.objects.all())
        if not Watchlist.objects.filter(listing=title):
            new_item = Watchlist(pk=title ,listing=title, addRemove=True)
            new_item.save()

        else:
            for objects in Watchlist.objects.filter(listing=title):
                if objects.listing == title and objects.addRemove == True:
                    Watchlist(listing=title).delete()

        print("Going out of POST", Watchlist.objects.all())

    try:    
        return render(request, "auctions/watchlist.html", {
            "watchlist_items": Watchlist.objects.all().reverse()
        })
    
    except OperationalError:
        return render(request, "auctions/watchlist.html", {
            "watchlist_items": None
        })
    
    