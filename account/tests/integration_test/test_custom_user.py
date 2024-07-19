from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from dev.test.fake_data.models.fake_account_models import FakeCustomUser


class CustomUserSignUpTestCase(APITestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.sign_up_url = reverse("sign-up")

    def test_pass_sign_up(self):
        # Arrange
        initial_user_count = get_user_model().objects.count()
        self.new_user = FakeCustomUser()

        data = self.new_user.required_fields

        # Act
        response = self.client.post(self.sign_up_url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], data["email"])
        self.assertEqual(get_user_model().objects.count(), initial_user_count + 1)

    def test_fail_sign_up_with_too_long_email(self):
        # Arrange
        ...

    def test_fail_sign_up_with_too_short_email(self):
        # Arrange
        ...

    def test_fail_sign_up_with_duplicated_email(self):
        # Arrange
        ...

    def test_fail_sign_up_with_invalid_email(self):
        # Arrange
        ...

    def test_fail_sign_up_with_data_without_email(self):
        # Arrange
        ...

    def test_fail_sign_up_with_too_short_password(self):
        # Arrange
        ...

    def test_fail_sign_up_with_too_long_password(self):
        # Arrange
        ...

    def test_fail_sign_up_with_password_without_number(self):
        # Arrange
        ...

    def test_fail_sign_up_with_password_without_alphabet(self):
        # Arrange
        ...

    def test_fail_sign_up_with_data_without_password(self):
        # Arrange
        ...
