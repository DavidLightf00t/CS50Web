from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listings(models.Model):
    #Think What a Listing consists of.
    # Title
    # Description
    # Picture

    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=False)
    photo = models.URLField(default="https://t4.ftcdn.net/jpg/04/70/29/97/360_F_470299797_UD0eoVMMSUbHCcNJCdv2t8B2g1GVqYgs.jpg", blank=False)
    category = models.CharField(max_length=64, blank=True)
    starting_bid = models.FloatField(max_length=64, default=0, blank=False)

    def __str__(self):
        return self.title

class Bids(models.Model):
    pass

class Comments(models.Model):
    pass
