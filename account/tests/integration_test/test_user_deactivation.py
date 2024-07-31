from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


class UserDeactivationTestCase(APITestCase):
    def setUp(self):
        self.user_info = {
            "email": "testuser@example.com",
            "password": "TestPassword123!",
        }
        self.user = User.objects.create_user(**self.user_info)
        self.deactivation_url = reverse("user-deactivation")
        self.signin_url = reverse("user-signin")

    def test_successful_account_deactivation(self):
        # Given
        self.client.force_authenticate(user=self.user)
        # When
        response = self.client.post(self.deactivation_url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_fail_login_with_deactivated_account(self):
        # Given
        self.user.is_active = False
        self.user.save()

        # When
        response = self.client.post(self.signin_url, self.user_info)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_deactivation_preserves_user_data(self):
        # Given
        self.client.force_authenticate(user=self.user)
        # When
        self.client.post(self.deactivation_url)

        # Then
        deactivated_user = User.objects.get(email=self.user_info["email"])
        self.assertFalse(deactivated_user.is_active)
        self.assertEqual(deactivated_user.email, self.user_info["email"])

    def test_unauthorized_deactivation_attempt(self):
        # Given
        # User is not authenticated

        # When
        response = self.client.post(self.deactivation_url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deactivation_logs_timestamp(self):
        # Given
        self.client.force_authenticate(user=self.user)

        # When
        response = self.client.post(self.deactivation_url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.deactivated_at)

    def test_deactivation_with_reason(self):
        # Given
        self.client.force_authenticate(user=self.user)
        reason = "Taking a break from the platform"

        # When
        response = self.client.post(self.deactivation_url, {"reason": reason})

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.deactivation_reason, reason)
