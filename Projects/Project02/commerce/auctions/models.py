from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    pass


class Listings(models.Model):
    # Think What a Listing consists of.
    # Title
    # Description
    # Picture
    # Time the listing was made

    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=False)
    photo = models.URLField(default="https://t4.ftcdn.net/jpg/04/70/29/97/360_F_470299797_UD0eoVMMSUbHCcNJCdv2t8B2g1GVqYgs.jpg", blank=False)
    category = models.CharField(max_length=64, blank=True)
    starting_bid = models.FloatField(max_length=64, default=0, blank=False)
    number_of_bids = models.FloatField(max_length=8, default=0)
    time_of_listing = models.DateTimeField(auto_now_add=True)

    # How the object names itself in the admin dashboard
    def __str__(self):
        return self.title

class Bids(models.Model):
    # Think of What Info you Might Need for a Bid
    # Bid Amount
    # Name of Bidder
    # Item Being Bid On

    bid_amount = models.FloatField(max_length=10, blank=False, default=0)
    name = models.CharField(max_length=64, blank=False, default=None)
    item = models.CharField(max_length=64, blank=False, default=None)

    def __str__(self):
        return f"Item: {self.item}"

class Comments(models.Model):
    # Think of What Info you Might Need for a Comment
    # Name of Commenter
    # The Comment Itself
    # The Item the Comment is On

    name = models.CharField(max_length=64, default=None)
    comment = models.TextField(max_length=1000, default=None)

class Watchlist(models.Model):
    # Think of what info you might need for a watchlist
    # Title of Listing
    # A bool to check if the item is in watchlist already to add and remove from watchlist

    listing = models.CharField(primary_key="title", max_length=64, blank=True, default="")
    addRemove = models.BooleanField(default=False)

    def __str__(self):
        return self.listing

