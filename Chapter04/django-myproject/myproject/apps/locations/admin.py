# -*- coding: utf-8 -*-
from django.contrib.gis import admin
from .models import Location
__author__ = 'Alan Hou'


@admin.register(Location)
class LocationAdmin(admin.OSMGeoAdmin):
    pass