from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


class AuthUrlTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="Test@123"
        )
        self.user.is_verified=True
        self.user.save()

    def authenticate(self):
        response = self.client.post(
            reverse("token-obtain-pair"),
            {
                "username": "test",
                "password": "Test@123",
            },
            format="json",
        )

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    
    def test_shorten_url_success(self):
        self.authenticate()
        response = self.client.post(
            reverse('shorten'),
            {
                "original_url": "https://google.com"
            },
            format="json"
        )
        self.assertEqual(response.status_code,201)
        self.assertIn("short_url", response.data)

    def test_shorten_url_autheticate_failed(self):
        response = self.client.post(
            reverse('shorten'),
            {
                "original_url": "https://google.com"
            },
            format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_redirect_success(self):
        self.authenticate()
        response = self.client.post(
            reverse("shorten"),
            {"original_url": "https://google.com"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        code = response.data["short_code"]
        redirect_response = self.client.get(
            reverse("redirecturl", kwargs={"code": code})
        )

        self.assertIn(redirect_response.status_code, [301, 302])

    def test_redirect_failed(self):
        self.authenticate()
        code = "response.data"
        redirect_response = self.client.get(
            reverse("redirecturl", kwargs={"code": code})
        )
        self.assertIn(redirect_response.status_code,[400,404])

    def test_shorten_missing_url(self):
        self.authenticate()
        response = self.client.post(
            reverse("shorten"),
            {},
            format="json"
        )
        self.assertEqual(response.status_code, 400)