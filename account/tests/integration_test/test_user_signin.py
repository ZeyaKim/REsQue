from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class UserSignInTestCase(APITestCase):
    def setUp(self):
        self.user_info = {"email": "testuser@email.com", "password": "TestPassword123!"}

        self.user = User.objects.create_user(**self.user_info)
        self.url = reverse("user-signin")

    def test_success_login_with_valid_credentials(self):
        """
        Test user can login with valid credentials
        """

        # When
        response = self.client.post(self.url, self.user_info)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_fail_login_with_invalid_password(self):
        # Given
        self.user_info["password"] = "InvalidPassword123!"

        # When
        response = self.client.post(self.url, self.user_info)

        # Then
        self.assertEqual(response.status_code, 400)

    def test_fail_login_with_nonexistent_account(self):
        # Given
        self.user_info["email"] = "nonexistuser@email.com"

        # When
        response = self.client.post(self.url, self.user_info)

        # Then
        self.assertEqual(response.status_code, 400)
