from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.newListing, name="newListing"),
    path("categories", views.category_view, name="category_view"),
    path("auctions/<str:listing_id>", views.listing, name="listing"),
    path("auctions/", views.new_bid, name="new_bid"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/<str:category>", views.category_listings, name="category_listings"),
    path("search/", views.search, name="search"),
    path("user/<str:user>", views.user_profile, name="user_profile"),
    path("comment/", views.new_comment, name="new_comment"),
    path("AuctionEnded/<str:listing_id>", views.end_auction, name="end_auction")
]
