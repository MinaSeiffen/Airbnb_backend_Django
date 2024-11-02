from django.urls import path
from . import api

urlpatterns = [
    path("", api.properties_list, name="properties_list"),
    path("create/", api.create_property, name="create_properties"),
    path("<uuid:pk>/", api.property_detail, name="properties_detail"),
    path("<uuid:pk>/book/", api.book_property, name="book_property"),
]