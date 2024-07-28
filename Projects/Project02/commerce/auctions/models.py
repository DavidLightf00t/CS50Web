from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    # Think of what a User might consist of
    # Watchlist
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
    time_of_listing = models.TimeField(default=None)

    def __str__(self):
        return self.title

class Bids(models.Model):
    # Think of What Info you Might Need for a Bid
    # Bid Amount
    # Name of Bidder
    # Item Being Bid On

    bid = models.FloatField(max_length=10, blank=False, default=0)
    name = models.CharField(max_length=64, blank=False, default=None)
    item = models.CharField(max_length=64, blank=False, default=None)

class Comments(models.Model):
    # Think of What Info you Might Need for a Comment
    # Name of Commenter
    # The Comment Itself
    # The Item the Comment is On

    name = models.CharField(max_length=64, default=None)
    comment = models.TextField(max_length=1000, default=None)
