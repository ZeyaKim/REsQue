from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectCreationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test1234@example.com", password="Password123!"
        )
        self.project_creation_url = reverse("project-list")

    def create_valid_project_data(self):
        return {
            "title": "Test Project",
            "description": "This is a test project.",
        }

    def test_successful_project_creation(self):
        # Given
        valid_project_data = self.create_valid_project_data()
        self.client.force_authenticate(self.user)

        # When
        response = self.client.post(self.project_creation_url, valid_project_data)

        # Then
        self.assertEqual(response.status_code, 201)

    def test_project_creation_with_empty_title(self):
        # Given
        invalid_project_data = self.create_valid_project_data()
        invalid_project_data["title"] = ""
        self.client.force_authenticate(self.user)

        # When
        response = self.client.post(self.project_creation_url, invalid_project_data)

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["title"][0], "This field may not be blank.")

    def test_project_creation_with_too_long_title(self):
        # Given
        invalid_project_data = self.create_valid_project_data()
        invalid_project_data["title"] = "a" * 101
        self.client.force_authenticate(self.user)

        # When
        response = self.client.post(self.project_creation_url, invalid_project_data)

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["title"][0],
            "Ensure this field has no more than 100 characters.",
        )

    def test_project_creation_with_too_long_description(self):
        # Given
        invalid_project_data = self.create_valid_project_data()
        invalid_project_data["description"] = "a" * 1001
        self.client.force_authenticate(self.user)

        # When
        response = self.client.post(self.project_creation_url, invalid_project_data)

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["description"][0],
            "Ensure this field has no more than 1000 characters.",
        )

    def test_project_creation_without_authentication(self):
        # Given
        valid_project_data = self.create_valid_project_data()

        # When
        response = self.client.post(self.project_creation_url, valid_project_data)

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
