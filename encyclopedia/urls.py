from django.urls import path

from . import views
from . import util
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.create_entry, name="new_entry"),
    path("wiki/<str:entry>", views.title, name="entry"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("random", views.random, name="random")
    ]


