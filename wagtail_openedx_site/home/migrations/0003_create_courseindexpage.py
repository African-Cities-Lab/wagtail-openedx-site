# -*- coding: utf-8 -*-
from django.db import migrations


def create_courseindexpage(apps, schema_editor):
    from wagtail_openedx_site.home.models import HomePage

    # Get models
    ContentType = apps.get_model("contenttypes.ContentType")
    # HomePage = apps.get_model("home.HomePage")
    CourseIndexPage = apps.get_model("wagtail_openedx.CourseIndexPage")

    # Create content type for the course index page model
    courseindexpage_content_type, __ = ContentType.objects.get_or_create(
        model="courseindexpage", app_label="wagtail_openedx"
    )

    # Get the home page
    homepage = HomePage.objects.get(
        slug="home",
    )
    # Create the course index page as a child of the home page
    # TODO: handle locales for multi-language sites
    slug = "courses"
    course_index_page = CourseIndexPage(
        title="Courses",
        slug=slug,
        url_path=homepage.url_path + slug + "/",
        content_type=courseindexpage_content_type,
        locale_id=1,
    )
    homepage.add_child(instance=course_index_page)
    # TODO: use `save` method to avoid duplicating logic (e.g., setting `url_path`)
    # course_index_page.save_revision().publish()


def remove_courseindexpage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model("contenttypes.ContentType")
    CourseIndexPage = apps.get_model("wagtail_opendx.CourseIndexPage")

    # Delete the course index page
    # Page and Site objects CASCADE
    CourseIndexPage.objects.get(slug="courses").delete()

    # Delete content type for homepage model
    ContentType.objects.filter(
        model="courseindexpage", app_label="wagtail_openedx"
    ).delete()


class Migration(migrations.Migration):

    # see https://github.com/wagtail/wagtail/issues/6557
    # run_before = [
    #     ("wagtailcore", "0053_locale_model"),
    # ]

    dependencies = [
        ("home", "0002_create_homepage"),
        ("wagtail_openedx", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_courseindexpage, remove_courseindexpage),
    ]
