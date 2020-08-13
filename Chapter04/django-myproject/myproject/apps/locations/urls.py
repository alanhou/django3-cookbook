# -*- coding: utf-8 -*-
from django.urls import path
from .views import LocationList, LocationDetail, add_or_change_location
__author__ = 'Alan Hou'

urlpatterns = [
    path("", LocationList.as_view(), name="location_list"),
    path("<uuid:pk>/", LocationDetail.as_view(), name="location_detail"),
    path(
        "<uuid:pk>/modal/",
        LocationDetail.as_view(template_name="locations/location_detail_modal.html"),
        name="location_detail_modal",
    ),
    path("<uuid:pk>/change/", add_or_change_location, name="add_or_change_location"),
]
