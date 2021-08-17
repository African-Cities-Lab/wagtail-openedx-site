from django import forms
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, TranslatableMixin
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

COURSE_CODE_MAX_LENGTH = 100
DEFAULT_CHAR_FIELD_MAX_LENGTH = 255


class OrganizationIndexPage(Page):
    pass


class OrganizationPage(Page):
    code = models.CharField(max_length=COURSE_CODE_MAX_LENGTH, verbose_name=_("code"))
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("logo"),
    )
    description = RichTextField(verbose_name=_("description"))

    content_panels = Page.content_panels + [
        FieldPanel("code"),
        ImageChooserPanel("logo"),
        FieldPanel("description", classname="full"),
    ]


class PersonIndexPage(Page):
    pass


class PersonPage(Page):
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("person"),
    )
    organization = ParentalManyToManyField(
        "courses.OrganizationPage", verbose_name=_("organization")
    )
    picture = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("picture"),
    )
    bio = RichTextField(verbose_name=_("short bio"))

    content_panels = Page.content_panels + [
        FieldPanel("person"),
        FieldPanel("organization"),
        ImageChooserPanel("picture"),
        FieldPanel("bio", classname="full"),
    ]


@register_snippet
class Category(TranslatableMixin, models.Model):
    name = models.CharField(
        max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH, verbose_name=_("name")
    )
    panels = [FieldPanel("name")]

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = _("category")
        verbose_name_plural = _("categories")


# TODO: class Program?


class CourseIndexPage(Page):
    pass


class CoursePage(Page):
    code = models.CharField(max_length=COURSE_CODE_MAX_LENGTH, verbose_name=_("code"))

    description = RichTextField(verbose_name=_("description"))

    categories = ParentalManyToManyField("courses.Category")
    instructors = ParentalManyToManyField(
        "courses.PersonPage", verbose_name=_("instructors")
    )

    content_panels = Page.content_panels + [
        FieldPanel("description", classname="full"),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
    ]
