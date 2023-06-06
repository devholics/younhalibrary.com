from django.shortcuts import reverse
from django.test import override_settings

from rest_framework import status
from rest_framework.test import APITestCase


@override_settings(ROOT_URLCONF="younha.urls.api")
class TestGalleryAPI(APITestCase):
    fixtures = ["medialib_gallery_data.json"]

    def test_get_creator_list(self):
        response = self.client.get(reverse("creator-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_get_creator_detail(self):
        response = self.client.get(reverse("creator-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse("creator-gallery", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 9)
        response = self.client.get(reverse("creator-detail", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_make_source(self):
        response = self.client.post(reverse("source-list"), {
            "url": "https://pixabay.com/ko/users/max_gindele_photography-24136281/",
            "title": "Max_Gindele_Photography",
            "description": ""
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_make_file_media(self):
        response = self.client.post(reverse("file_media-list"), {
            "type": "I",
            "thumbnail_url": "",
            "url": "https://cdn.pixabay.com/photo/2023/01/25/22/46/grey-reef-shark-7744765__480.jpg",
            "creator": 1,
            "date": "2023-01-01",
            "source": "https://pixabay.com/ko/users/jbooba-23039065/",
            "tags": [],
            "date_exact": True,
            "license": "Pixabay",
            "verified": True,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse("creator-gallery", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_bulk_create_file_media(self):
        response = self.client.post(reverse("file_media-bulk-create"), [
            {
                "type": "I",
                "thumbnail_url": "",
                "url": "https://cdn.pixabay.com/photo/2023/01/25/22/46/grey-reef-shark-7744765__480.jpg",
                "creator": 1,
                "date": "2023-01-01",
                "source": "https://pixabay.com/ko/users/jbooba-23039065/",
                "tags": [],
                "date_exact": True,
                "license": "Pixabay",
                "verified": True,
            },
            {
                "type": "I",
                "thumbnail_url": "",
                "url": "https://cdn.pixabay.com/photo/2022/09/28/06/11/water-7484334__480.jpg",
                "creator": 1,
                "date": "2023-01-01",
                "source": "https://pixabay.com/ko/users/jbooba-23039065/",
                "tags": [],
                "date_exact": True,
                "license": "Pixabay",
                "verified": True,
            }
        ], format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse("creator-gallery", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 11)
