from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import uuid

User = get_user_model()


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.verified_user = User.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="Test@123",
            is_verified=True
        )
        self.unverified_user = User.objects.create_user(
            username="test1",
            email="test1@gmail.com",
            password="Test@123"
        )

    def test_login_unverified_failed(self):
        response = self.client.post(
            reverse("token-obtain-pair"),
            {
                "username": "test1",
                "password": "Test@123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_register_success(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "test5",
                "password": "Test@123",
                "email":"test5@gmail.com",
                "password2":"Test@123"
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_register_failed(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "test",
                "password": "Test@123",
                "email":"test@gmail.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
            
    def test_login_success(self):
        response = self.client.post(
            reverse("token-obtain-pair"),
            {
                "username": "test",
                "password": "Test@123",
            },
            format="json",
        )

        self.assertEqual(response.status_code,200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failed(self):
        response = self.client.post(
            reverse("token-obtain-pair"),
            {
                "username": "test",
                "password": "Test123",
            },
            format="json",
        )

        self.assertEqual(response.status_code,401)
    
    def test_verify_email(self):
        token = self.unverified_user.verification_token 

        url = reverse("verify-email", kwargs={"token": token})

        response = self.client.get(url)

        self.assertTrue(response.status_code,200)

    def test_verify_email_failed(self):
        token = uuid.uuid4()
        url = reverse("verify-email", kwargs={"token": token})
        response = self.client.get(url)
        self.assertTrue(response.status_code,400)
    
    def test_refresh_success(self):
        login_response = self.client.post(
            reverse("token-obtain-pair"),
            {
                "username": "test",
                "password": "Test@123",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code,200)

        refresh_token = login_response.data["refresh"]

        refresh_response = self.client.post(
            reverse("token-refresh"),
            {"refresh": refresh_token},
            format="json"
        )

        self.assertEqual(refresh_response.status_code,200)
        self.assertIn("access", refresh_response.data)
    
    def test_refresh_failed(self):
        refresh_response = self.client.post(
            reverse("token-refresh"),
            {"refresh": "invalid_token"},
            format="json"
        )

        self.assertEqual(refresh_response.status_code,401 )
    
    def test_profile_success(self):
        login_response = self.client.post(
            reverse("token-obtain-pair"),
            {
                "username": "test",
                "password": "Test@123",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code,200)

        access_token = login_response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code,200)

    def test_profile_fail_no_token(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 401)

    def test_profile_fail_invalid_token(self):
    
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer abs.cdjsmfh"
        )
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 401)

    def test_logout_success(self):
        
        login_response = self.client.post(
            reverse("token-obtain-pair"),
            {
                "username": "test",
                "password": "Test@123",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, 200)

        refresh_token = login_response.data["refresh"]
        response = self.client.post(
            reverse("token-blacklist"),
            {
                "refresh": refresh_token
            },
            format="json"
        )

        self.assertIn(response.status_code, [200, 205])
    
    def test_logout_failed(self):
        response = self.client.post(
            reverse("token-blacklist"),
            {
                "refresh": "refresh_token"
            },
            format="json"
        )

        self.assertTrue(response.status_code,401)