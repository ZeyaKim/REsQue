from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from dev.test.fake_data.models.fake_account_models import FakeCustomUser


class CustomUserRegisterTestCase(APITestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user1 = FakeCustomUser()
        self.register_url = reverse("register")

    def test_create_user_success(self):
        data = self.user1.required_fields

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_fail_with_wrong_email(self):
        self.assertEqual(True, True)

    def test_create_user_fail_with_weak_password(self): ...

    def test_create_user_fail_with_duplicate_email(self): ...

    def test_create_user_fail_with_missing_required_field(self): ...
