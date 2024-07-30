from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone

User = get_user_model()


class UserDeactivationTest(APITestCase):
    def setUp(self):
        self.user_info = {
            "email": "testuser@example.com",
            "password": "TestPassword123!",
        }
        self.user = User.objects.create_user(**self.user_info)
        self.url = reverse("user-deactivation")

    def test_successful_account_deactivation(self):
        # Given
        self.client.force_authenticate(user=self.user)

        # When
        response = self.client.post(self.url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_login_attempt_with_deactivated_account(self):
        # Given
        self.user.is_active = False
        self.user.save()

        # When
        response = self.client.post(reverse("token_obtain_pair"), self.user_info)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deactivation_preserves_user_data(self):
        # Given
        self.client.force_authenticate(user=self.user)

        # When
        response = self.client.post(self.url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(email=self.user_info["email"]).exists())
        deactivated_user = User.objects.get(email=self.user_info["email"])
        self.assertFalse(deactivated_user.is_active)

    def test_deactivation_logs_timestamp(self):
        # Given
        self.client.force_authenticate(user=self.user)

        # When
        response = self.client.post(self.url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.deactivated_at)
        self.assertAlmostEqual(
            self.user.deactivated_at,
            timezone.now(),
            delta=timezone.timedelta(seconds=1),
        )

    def test_deactivation_with_reason(self):
        # Given
        self.client.force_authenticate(user=self.user)
        reason = "Taking a break from the platform"

        # When
        response = self.client.post(self.url, {"reason": reason})

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.deactivation_reason, reason)

    def test_unauthorized_deactivation_attempt(self):
        # Given
        # User is not authenticated

        # When
        response = self.client.post(self.url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reactivation_not_allowed(self):
        # Given
        self.user.is_active = False
        self.user.save()
        self.client.force_authenticate(user=self.user)

        # When
        response = self.client.post(reverse("user-activation"))

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
