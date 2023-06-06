from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class TestGallery(TestCase):
    def test_index(self):
        response = self.client.get(reverse("filemedia-list"))
        self.assertEqual(response.status_code, 200)
