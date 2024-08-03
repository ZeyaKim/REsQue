from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class UserSignInTestCase(APITestCase):
    def setUp(self):
        self.user_info = {
            "email": "testuser@example.com",
            "password": "TestPassword123!",
        }

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
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_fail_login_with_invalid_password(self):
        # Given
        self.user_info["password"] = "InvalidPassword123!"

        # When
        response = self.client.post(self.url, self.user_info)

        # Then
        self.assertEqual(response.status_code, 401)

    def test_fail_login_with_nonexistent_account(self):
        # Given
        self.user_info["email"] = "nonexistuser@email.com"

        # When
        response = self.client.post(self.url, self.user_info)

        # Then
        self.assertEqual(response.status_code, 400)


class UserSignInEdgeCaseTestCase(APITestCase):
    def setUp(self):
        self.user_info = {"email": "testuser@email.com", "password": "TestPassword123!"}
        self.user = User.objects.create_user(**self.user_info)
        self.url = reverse("user-signin")

    def test_fail_login_with_case_sensitive_email(self):
        # Given
        self.user_info["email"] = self.user_info["email"].upper()

        # When
        response = self.client.post(self.url, self.user_info)

        # Then
        self.assertEqual(response.status_code, 400)

    def test_fail_login_with_spaces_in_email(self):
        # Given
        self.user_info["email"] = f" {self.user_info['email']} "

        # When
        response = self.client.post(self.url, self.user_info)

        # Then
        self.assertEqual(response.status_code, 400)

    def test_fail_login_with_inactive_user(self):
        # Given
        new_user_info = {
            "email": "newuser@example.com",
            "password": "TestPassword123!",
        }
        new_user = User.objects.create_user(**new_user_info, is_active=False)

        # When
        response = self.client.post(self.url, new_user_info)

        # Then
        self.assertEqual(response.status_code, 401)

    def test_fail_login_with_maximum_length_email(self):
        # Given
        self.user_info["email"] = "a" * 242 + "@email.com"  # 총 254자

        # When
        response = self.client.post(self.url, self.user_info)

        # Then
        self.assertEqual(response.status_code, 400)

    def test_fail_login_with_minimum_length_password(self):
        # Given
        self.user_info["password"] = "Aa1!"  # 최소 길이 비밀번호

        # When
        response = self.client.post(self.url, self.user_info)

        # Then
        self.assertEqual(response.status_code, 400)

    def test_fail_login_with_special_characters_in_email(self):
        # Given
        self.user_info["email"] = "test.user+special@email.com"

        # When
        response = self.client.post(self.url, self.user_info)

        # Then
        self.assertEqual(response.status_code, 400)

    def test_fail_login_with_unicode_characters_in_password(self):
        # Given
        self.user_info["password"] = "TestPassword123!안녕😀"

        # When
        response = self.client.post(self.url, self.user_info)

        # Then
        self.assertEqual(response.status_code, 400)
