from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from myproject.apps.core.models import (
    CreationModificationDateBase,
    MetaTagsBase,
    UrlBase,
)
from myproject.apps.core.model_fields import (
    MultilingualCharField,
    MultilingualTextField
)

class Idea(CreationModificationDateBase, MetaTagsBase, UrlBase):
    title = MultilingualCharField(_("Title"), max_length=200)
    content = MultilingualTextField(_("Content"))
    # category = models.ForeignKey(
    #     "categories.Category",
    #     verbose_name=_("Category"),
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     related_name="category_ideas",
    # )
    categories = models.ManyToManyField(
        "categories.Category",
        verbose_name=_("Categories"),
        blank=True,
        related_name="ideas",
    )

    class Meta:
        verbose_name = _("Idea")
        verbose_name_plural = _("Ideas")

    def __str__(self):
        return self.title

    def get_url_path(self):
        return reverse("idea_details", kwargs={
            "idea_id": str(self.pk)
        })
