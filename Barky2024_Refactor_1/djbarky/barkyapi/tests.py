from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework import routers
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Bookmark
from .views import BookmarkViewSet

# Create your tests here.
# test plan


class BookmarkTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.bookmark = Bookmark.objects.create(
            id=1,
            title="Awesome Django",
            url="https://awesomedjango.org/",
            notes="Best place on the web for Django.",
        )
        # print(f"bookmark id: {self.bookmark.id}")

        # the simple router provides the name 'bookmark-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:bookmark-list")
        self.detail_url = reverse(
            "barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}
        )

    # 1. create a bookmark
    def test_create_bookmark(self):
        """
        Ensure we can create a new bookmark object.
        """

        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Django REST framework",
            "url": "https://www.django-rest-framework.org/",
            "notes": "Best place on the web for Django REST framework.",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Bookmark.objects.count(), 2)
        self.assertEqual(Bookmark.objects.get(
            id=99).title, "Django REST framework")

    # 2. list bookmarks
    def test_list_bookmarks(self):
        """
        Ensure we can list all bookmark objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"]
                         [0]["title"], self.bookmark.title)

    # 3. retrieve a bookmark
    def test_retrieve_bookmark(self):
        """
        Ensure we can retrieve a bookmark object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], self.bookmark.title)

    # 4. delete a bookmark
    def test_delete_bookmark(self):
        """
        Ensure we can delete a bookmark object.
        """
        response = self.client.delete(
            reverse("barkyapi:bookmark-detail",
                    kwargs={"pk": self.bookmark.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 0)

    # 5. update a bookmark
    def test_update_bookmark(self):
        """
        Ensure we can update a bookmark object.
        """
        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Awesomer Django",
            "url": "https://awesomedjango.org/",
            "notes": "Best place on the web for Django just got better.",
        }
        response = self.client.put(
            reverse("barkyapi:bookmark-detail",
                    kwargs={"pk": self.bookmark.id}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], "Awesomer Django")

    # 6. Create a snippet
    def test_create_snippet(self):
        data = {
            "title": 'New Snippet',
            "url": "https://awesomedjango.org/",
            "code": "print('Barky snippet')",
            ".pytest_cache/owner": self.user.id
        }
        response = self.client.post(self.snippet_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Snippet.objects.count(), 2)
        self.assertEqual(Snippet.objects.latest('id').title, 'New Snippet')

    # 7. Retrieve a snippet
    def test_retrieve_snippet(self):
        response = self.client.get(self.snippet_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.snippet.title)

     # 8. Delete a snippet
    def test_delete_snippet(self):
        response = self.client.delete(self.snippet_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 0)

    # 9. List snippets
    def test_list_snippets(self):
        response = self.client.get(self.snippet_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.snippet.title)

    # 10. Update a snippet
    def test_update_snippet(self):
        updated_data = {
            "title": "Updated Snippet",
            "code": "print('newer snippet')",
            "owner": self.user.id
        }
        response = self.client.put(
            self.snippet_detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Snippet.objects.get(
            id=self.snippet.id).title, "newer Snippet")

    # 11. Create a user
    def test_create_user(self):
        user_data = {
            "username": "new",
            "email": "new@yahoo.com",
            "password": "password123"
        }
        response = self.client.post(
            self.user_list_url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DjangoUser.objects.count(), 2)
        self.assertEqual(DjangoUser.objects.get(
            username='new').email,  "new@yahoo.com")
