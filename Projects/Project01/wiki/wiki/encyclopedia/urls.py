from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.newPage, name="newPage"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/", views.search, name="search"),
    path("random/", views.random, name="random"),
    path("edit/" , views.editPage, name="edit"),
    path("savePage", views.savePage, name="savePage")
]
