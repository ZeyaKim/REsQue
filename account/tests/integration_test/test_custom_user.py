from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from dev.test.fake_data.models.fake_account_models import FakeCustomUser
from django.core.management import call_command


class CustomUserRegisterTestCase(APITestCase):
    fixtures = ["test_users.json"]

    @classmethod
    def setUpTestData(cls):
        cls.user_model = get_user_model()
        cls.register_url = reverse("register")

    def setUp(self):
        call_command("loaddata", "fixtures/test_users.json", verbosity=0)
        self.user1 = FakeCustomUser()

    def test_register_success(self):
        data = self.user1.required_fields

    def test_register_fail_with_wrong_email(self): ...

    def test_register_fail_with_weak_password(self): ...

    def test_register_fail_with_duplicate_email(self): ...

    def test_register_fail_with_missing_required_field(self): ...
