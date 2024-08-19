from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from sqlite3 import OperationalError

import uuid

from .models import User, Listings, Bids, Comments, Watchlist


def index(request):
    objects = Listings.objects.all()

    for listings in objects:
        print(listings.listing_id)

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

        unique_id = uuid.uuid1()
        print(unique_id)

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
            new_listing = Listings(listing_id=unique_id, title=title, description=description, photo=url, category=category, starting_bid=starting_bid, number_of_bids=0)
            new_listing.save()
        
        if not url:
            new_listing = Listings(listing_id=unique_id, title=title, description=description, category=category, starting_bid=starting_bid, number_of_bids=0)
            new_listing.save()
        
        if not category:
            new_listing = Listings(listing_id=unique_id, title=title, description=description, photo=url, starting_bid=starting_bid, number_of_bids=0)
            new_listing.save()

        
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "auctions/newListing.html")
    

def listing(request, listing_id):
    try:
        listing = Listings.objects.get(listing_id=listing_id)
        bid_info = Bids.objects.filter(listing=listing).latest('id')

        #Returns all of the info of the listing model. Title, Description, Photo Url, Category, and Starting Bid
        return render(request, "auctions/auctions.html", {
            "listing_info": Listings.objects.get(listing_id=listing_id),
            "bid_info": bid_info
        })
    except ObjectDoesNotExist:
        bid_info = None
        
        return render(request, "auctions/auctions.html", {
                "listing_info": Listings.objects.get(listing_id=listing_id),
                "bid_info": bid_info
            })

def new_bid(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        new_bid = request.POST["bid"]
        listing = Listings.objects.get(listing_id=listing_id)

        # We need to make the new bid into a float (originally a string)
        new_bid = float(new_bid)

        #Get User objects
        user = request.user.get_username()
        user = User.objects.get(username=user)

        if user is not "":
            # We then need to compare the new bid passed to the current bid
            # If the new bid is greater update if not error
            if new_bid <= listing.starting_bid:
                return render(request, "auctions/auctions.html", {
                    "listing_info": Listings.objects.get(listing_id=listing_id),
                    "message": "New Bid MUST be larger than current bid"
                })

            #Now that all of the bid info has been gotten, make a bid object then save it
            bid_object = Bids(bidder=user, bid_amount=new_bid, listing=listing)
            bid_object.save()

            #TODO Make User info model work

            # Increase number of bids
            listing.number_of_bids = listing.number_of_bids + 1
            listing.save()

            #Assign and save new bid
            listing.starting_bid = new_bid
            listing.save()

            #Update number of bids
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "auctions/login.html", {
                "message": "Must Be Logged In to Place Bids"
            })
    
    return render(request, "auctions/auctions.html", {
        "listing_info": Listings.objects.get(listing_id=listing_id)
    })


def category_view(request):
    # Make a new list of all of the non repeating categories
    category_list = []
    for objects in Listings.objects.all():
        # if object in category_list:
        if objects.category not in category_list:
            category_list.append(objects.category)

    return render(request, "auctions/category_list.html", {
        "info": category_list,
    })

def watchlist(request):

    if request.method == "POST":
        user = request.user.get_username()
        user = User.objects.get(username=user)

        listing_id = request.POST["listing_id"]
        listing = Listings.objects.get(listing_id=listing_id)
        print(Watchlist.objects.filter(listing=listing))

        if not Watchlist.objects.filter(listing=listing):
            new_item = Watchlist(watcher=user, listing=listing, addRemove=True)
            new_item.save()

        else:
            for objects in Watchlist.objects.filter(listing=listing):
                if objects.listing == listing and objects.addRemove == True:
                    obj = Watchlist.objects.get(listing=listing)
                    obj.delete()


    try:

        for items in Watchlist.objects.all().reverse():
            print(items.listing)


        return render(request, "auctions/watchlist.html", {
            "watchlist_items": Watchlist.objects.all().reverse(),
        })
        
    except OperationalError:
        return render(request, "auctions/watchlist.html", {
            "watchlist_items": None
        })
    
def category_listings(request, category):
    return render(request, "auctions/category.html", {
        "listing": Listings.objects.filter(category=category),
        "category": category
    })

def search(request):
    if request.method == "POST":
        query = request.POST["query"]
        objects = Listings.objects.all()

        titles = []

        for listings in objects:
            if query.lower() in listings.title.lower():
                titles.append(listings)
            

        return render(request, "auctions/search.html", {
            "query": titles
        })