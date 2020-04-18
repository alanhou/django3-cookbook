from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from myproject.apps.core.model_fields import TranslatedField

class Idea(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=200,
    )
    content = models.TextField(
        _("Content"),
    )
    translated_title = TranslatedField("title")
    translated_content = TranslatedField("content")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        "categories.Category",
        verbose_name=_("Category"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = _("Idea")
        verbose_name_plural = _("Ideas")
        constraints = [
            models.UniqueConstraint(
                fields=["title"],
                condition=~models.Q(author=None),
                name="unique_titles_for_each_author",
            ),
            models.CheckConstraint(
                check=models.Q(
                    title__iregex=r"^\S.*\S$"
                    # starts with non-whitespace,
                    # ends with non-whitespace,
                    # anything in the middle
                ),
                name="title_has_no_leading_and_trailing_whitespaces",
            )
        ]

    def clean(self):
        import re
        if self.author and Idea.objects.exclude(pk=self.pk).fitler(
            author=self.author,
            title=self.title,
        ).exists():
            raise ValidationError(
                _("Each idea of the same user should have a unique title.")
            )
        if not re.match(r"^\S.*\S", self.title):
            raise ValidationError(
                _("The title cannot start or end with a whitespace.")
            )

    def __str__(self):
        return self.title


class IdeaTranslations(models.Model):
    idea = models.ForeignKey(
        Idea,
        verbose_name=_("Idea"),
        on_delete=models.CASCADE,
        related_name="translations",
    )
    language = models.CharField(_("Language"), max_length=7)

    title = models.CharField(
        _("Title"),
        max_length=200,
    )
    content = models.TextField(
        _("Content"),
    )

    class Meta:
        verbose_name = _("Idea Translations")
        verbose_name_plural = _("Idea Translations")
        ordering = ["language"]
        unique_together = [["idea", "language"]]

    def __str__(self):
        return self.title