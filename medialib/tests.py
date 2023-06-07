from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Creator


class TestGallery(TestCase):
    fixtures = ["medialib_gallery_data.json"]

    def test_index(self):
        response = self.client.get(reverse("filemedia-list"))
        self.assertEqual(response.status_code, 200)

    @override_settings(MEDIALIB_GALLERY_PAGINATION=5)
    def test_pagination_duplicate(self):
        response = self.client.get(reverse("creator-gallery", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        creator = response.context["creator"]
        self.assertEqual(creator.media_count(), 8)
        self.assertEqual(len(response.context["page_obj"]), 5)
        response = self.client.get(reverse("creator-gallery", kwargs={"pk": 1}), {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 3)


class TestYouTube(TestCase):
    def test_index(self):
        response = self.client.get(reverse("youtubevideo-list"))
        self.assertEqual(response.status_code, 200)
