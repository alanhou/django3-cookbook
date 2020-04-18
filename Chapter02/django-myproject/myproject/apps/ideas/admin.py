from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from myproject.apps.core.admin import get_multilingual_field_names

from .models import Idea

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Title and Content"), {
            "fields": get_multilingual_field_names("title") +
                get_multilingual_field_names("content")
        })
    ]