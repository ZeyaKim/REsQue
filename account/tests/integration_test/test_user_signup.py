from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSignupTestCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse("user-signup")

    def create_valid_data(self):
        return {"email": "newuser@example.com", "password": "SecurePass123"}

    def test_successful_signup(self):
        # Given
        data = self.create_valid_data()

        # When
        response = self.client.post(self.signup_url, data)

        # Then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=data["email"]).exists())
        self.assertEqual(User.objects.count(), 1)

    def test_signup_with_existing_email(self):
        # Given
        existing_user = User.objects.create_user(
            email="existing@example.com", password="password123"
        )
        data = self.create_valid_data()
        data["email"] = existing_user.email

        # When
        response = self.client.post(self.signup_url, data)

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("custom user의 email은/는 이미 존재합니다.", str(response.data))
        self.assertEqual(User.objects.count(), 1)

    def test_signup_with_invalid_email(self):
        # Given
        data = self.create_valid_data()
        data["email"] = "invalid-email"

        # When
        response = self.client.post(self.signup_url, data)

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("유효한 이메일 주소를 입력하십시오.", str(response.data))
        self.assertEqual(User.objects.count(), 0)

    def test_signup_without_password(self):
        # Given
        data = self.create_valid_data()
        data.pop("password")

        # When
        response = self.client.post(self.signup_url, data)

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("이 필드는 필수 항목입니다.", str(response.data))
        self.assertEqual(User.objects.count(), 0)

    def test_signup_with_short_password(self):
        # Given
        data = self.create_valid_data()
        data["password"] = "sho1t"

        # When
        response = self.client.post(self.signup_url, data)

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Password must contain 6 to 30 characters", str(response.data))
        self.assertEqual(User.objects.count(), 0)
