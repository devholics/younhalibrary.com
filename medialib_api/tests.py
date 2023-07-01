from django.test import override_settings

from rest_framework import status
from rest_framework.test import APITestCase


@override_settings(ROOT_URLCONF="younhalibrary.urls.api")
class TestGalleryAPI(APITestCase):
    fixtures = ["medialib_photo_data.json"]

    def test_get_creator_list(self):
        response = self.client.get("/creators/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_get_creator_detail(self):
        response = self.client.get("/creators/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get("/creators/1/gallery/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)
        response = self.client.get("/creators/2/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_make_source(self):
        response = self.client.post("/sources/", {
            "url": "https://pixabay.com/ko/users/max_gindele_photography-24136281/",
            "title": "Max_Gindele_Photography",
            "description": ""
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_make_photo(self):
        response = self.client.post("/photos/", {
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
        response = self.client.get("/creators/1/gallery/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 9)

    def test_bulk_create_photo(self):
        response = self.client.post("/photos/bulk_create/", [
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
        response = self.client.get("/creators/1/gallery/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_ordering(self):
        resp_default = self.client.get("/photos/")
        resp_reverse = self.client.get("/photos/?ordering=date,id")
        self.assertEqual(resp_default.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_reverse.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(reversed(resp_default.data["results"])), resp_reverse.data["results"])

    def test_search_title(self):
        response = self.client.get("/photos/?search=fly")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["count"], 2)

    def test_search_tag(self):
        response = self.client.get("/photos/?search=animal")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["count"], 8)

    def test_search_meaningless(self):
        response = self.client.get("/photos/?search=ejfeiojedoir")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_combined_filter(self):
        response = self.client.get("/photos/?search=animal&start_date=2022-03-01&end_date=2022-05-03&creator=1&tags=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data["count"], 0)

    def test_creator_ordering(self):
        response = self.client.get("/creators/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(response.data["results"][0]["id"], 1)

    def test_tag_ordering(self):
        response = self.client.get("/tags/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["id"], 1)

    def test_photo_detail_has_creator(self):
        response = self.client.get("/photos/2/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data["creator"], dict)

    def test_tag_counts(self):
        response = self.client.get("/tags/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["photo_count"], 7)
