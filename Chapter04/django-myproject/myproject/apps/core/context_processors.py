# -*- coding: utf-8 -*-
from django.conf import settings
__author__ = 'Alan Hou'


def website_url(request):
    return {
        "WEBSITE_URL": settings.WEBSITE_URL,
    }


def google_maps(request):
    return {
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
    }