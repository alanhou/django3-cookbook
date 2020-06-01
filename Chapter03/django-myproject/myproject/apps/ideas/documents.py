# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import get_language, activate
from django.db import models

from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.documents import (
    Document,
    model_field_class_to_field_class
)
from django_elasticsearch_dsl.registries import registry

from myproject.apps.categories.models import Category
from .models import Idea
__author__ = 'Alan Hou'

model_field_class_to_field_class[models.UUIDField] = fields.TextField


def _get_url_path(instance, language):
    current_language = get_language()
    activate(language)
    url_path = instance.get_url_path()
    activate(current_language)
    return url_path


@registry.register_document
class IdeaDocument(Document):
    author = fields.NestedField(
        properties={
            "first_name": fields.KeywordField(),
            "last_name": fields.KeywordField(),
            "username": fields.KeywordField(),
            "pk": fields.IntegerField(),
        },
        include_in_root = True,
    )
    # title_bg = fields.KeywordField()
    # title_hr = fields.KeywordField()
    # other title_* fields for each language in the LANGUAGES setting...
    # content_bg = fields.KeywordField()
    # content_hr = fields.KeywordField()
    # other content_* fields for each language in the LANGUAGES setting...

    picture_thumbnail_url = fields.KeywordField()
    categories = fields.NestedField(
        properties=dict(
            pk=fields.IntegerField(),
            # title_bg=fields.KeywordField(),
            # title_hr=fields.KeywordField(),
            # other title_* definitions for each language in the LANGUAGES setting...
        ),
        include_in_root=True,
    )
    # url_path_lt = fields.KeywordField()
    # url_path_hr = fields.KeywordField()
    # other url_path_* fields for each language in the LANGUAGES setting...

    class Index:
        name = "ideas"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Idea
        # The fields of the model you want to be indexed in Elasticsearch
        fields = ["uuid", "rating"]
        related_models = [Category]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            category = related_instance
            return category.category_ideas.all()

    def prepare(self, instance):
        lang_code_underscored = settings.LANGUAGE_CODE.replace("-", "_")
        setattr(instance, f"title_{lang_code_underscored}", instance.title)
        setattr(instance, f"content_{lang_code_underscored}", instance.content)
        setattr(instance, f"url_path_{lang_code_underscored}", _get_url_path(
            instance=instance, language=settings.LANGUAGE_CODE,
        ))
        for lang_code, lang_name in settings.LANGUAGES_EXCEPT_THE_DEFAULT:
            lang_code_underscored = lang_code.replace("-", "_")
            setattr(instance, f"title_{lang_code_underscored}", "")
            setattr(instance, f"content_{lang_code_underscored}", "")
            translations = instance.translations.filter(language=lang_code).first()
            if translations:
                setattr(instance, f"title_{lang_code_underscored}", translations.title)
                setattr(instance, f"content_{lang_code_underscored}", translations.content)
                setattr(instance, f"url_path_{lang_code_underscored}", _get_url_path(
                    instance=instance, language=lang_code
                ))
        data = super().prepare(instance=instance)
        return data

    def prepare_picture_thumbnail_url(self, instance):
        if not instance.picture:
            return ""
        return instance.picture_thumbnail.url

    def prepare_author(self, instance):
        author = instance.author
        if not author:
            return []
        author_dict = {
            "pk": author.pk,
            "first_name": author.first_name,
            "last_name": author.last_name,
            "username": author.username,
        }
        return [author_dict]

    def prepare_categories(self, instance):
        categories = []
        for category in instance.categories.all():
            category_dict = {"pk": category.pk}
            lang_code_underscored = settings.LANGUAGE_CODE.replace("-", "_")
            category_dict[f"title_{lang_code_underscored}"] = category.title
            for lang_code, lang_name in settings.LANGUAGES_EXCEPT_THE_DEFAULT:
                lang_code_underscored = lang_code.replace("-", "_")
                category_dict[f"title_{lang_code_underscored}"] = ""
                translations = category.translations.filter(language=lang_code).first()
                if translations:
                    category_dict[f"title_{lang_code_underscored}"] = translations.title
            categories.append(category_dict)
        return categories

    @property
    def translated_title(self):
        lang_code_underscored = get_language().replace("-", "_")
        return getattr(self, f"title_{lang_code_underscored}", "")

    @property
    def translated_content(self):
        lang_code_underscored = get_language().replace("-", "_")
        return getattr(self, f"content_{lang_code_underscored}", "")

    def get_url_path(self):
        lang_code_underscored = get_language().replace("-", "_")
        return getattr(self, f"url_path_{lang_code_underscored}", "")

    def get_categories(self):
        lang_code_underscored = get_language().replace("-", "_")
        return [
            dict(
                translated_title=category_dict[f"title_{lang_code_underscored}"],
                **category_dict,
            )
            for category_dict in self.categories
        ]