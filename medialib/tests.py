from django.test import TestCase
from django.urls import reverse

from .models import Creator


class TestGallery(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_index(self):
        response = self.client.get(reverse("filemedia-list"))
        self.assertEqual(response.status_code, 200)


class TestYouTube(TestCase):
    def test_index(self):
        response = self.client.get(reverse("youtubevideo-list"))
        self.assertEqual(response.status_code, 200)


class TestCreator(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.younha = Creator.objects.create(name="Younha")
        cls.c9ent = Creator.objects.create(name="C9Ent")

    def test_index(self):
        response = self.client.get(reverse("creator-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["creator_list"]), 2)
        response = self.client.get(reverse("creator-detail"), {"pk": self.younha.id})
        self.assertEqual(response.status_code, 200)


class TestTag(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_index(self):
        response = self.client.get(reverse("tag-list"))
        self.assertEqual(response.status_code, 200)

