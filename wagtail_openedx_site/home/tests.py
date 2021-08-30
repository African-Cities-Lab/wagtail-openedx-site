from django.test import TestCase
from wagtail.core.models import Site

from .models import HomePage


class HomePageCase(TestCase):
    def setUp(self):
        self.root_page = Site.objects.first().root_page

    def test_root_home_page(self):
        # test that the root page is a `HomePage` instance
        self.assertIsInstance(self.root_page.specific, HomePage)

    # TODO: test HomePage context
