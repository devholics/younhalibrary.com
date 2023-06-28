from django.test import TestCase, override_settings
from django.urls import reverse


class TestGallery(TestCase):
    fixtures = ["medialib_photo_data.json"]

    def test_index(self):
        response = self.client.get(reverse("photo-list"))
        self.assertEqual(response.status_code, 200)

    @override_settings(MEDIALIB_GALLERY_PAGINATION=5)
    def test_creator_pagination(self):
        response = self.client.get(reverse("creator-gallery", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        creator = response.context["creator"]
        self.assertEqual(creator.media_count(), 8)
        self.assertEqual(len(response.context["page_obj"]), 5)
        response = self.client.get(reverse("creator-gallery", kwargs={"pk": 1}), {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 3)


class TestYouTube(TestCase):
    fixtures = ["medialib_youtube_data.json"]

    def test_index(self):
        response = self.client.get(reverse("youtubevideo-list"))
        self.assertEqual(response.status_code, 200)

    @override_settings(MEDIALIB_YOUTUBE_PAGINATION=5)
    def test_creator_pagination(self):
        response = self.client.get(reverse("creator-youtube", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, 200)
        creator = response.context["creator"]
        self.assertEqual(creator.media_count(), 1)

        response = self.client.get(reverse("creator-youtube", kwargs={"pk": 27}))
        self.assertEqual(response.status_code, 200)
        creator = response.context["creator"]
        self.assertEqual(creator.media_count(), 7)
        self.assertEqual(len(response.context["page_obj"]), 5)
        response = self.client.get(reverse("creator-youtube", kwargs={"pk": 27}), {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 2)
