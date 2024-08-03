from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from project.models import Project

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
        self.assertEqual(response.data["title"][0], "이 필드는 blank일 수 없습니다.")

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
            "이 필드의 글자 수가 100 이하인지 확인하십시오.",
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
            "이 필드의 글자 수가 1000 이하인지 확인하십시오.",
        )

    def test_project_creation_without_authentication(self):
        # Given
        valid_project_data = self.create_valid_project_data()

        # When
        response = self.client.post(self.project_creation_url, valid_project_data)

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"],
            "자격 인증데이터(authentication credentials)가 제공되지 않았습니다.",
        )

    def test_duplicate_project_title(self):
        # Given
        valid_project_data = self.create_valid_project_data()
        Project.objects.create(**valid_project_data, founder=self.user)
        self.client.force_authenticate(self.user)

        # When
        response = self.client.post(self.project_creation_url, valid_project_data)

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertIn(
            "A project with this title already exists for this founder.",
            str(response.data["non_field_errors"]),
        )

    def test_project_creation_without_description(self):
        # Given
        data = {"title": "Test Project"}
        self.client.force_authenticate(self.user)

        # When
        response = self.client.post(self.project_creation_url, data)

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("description", response.data)
        self.assertIn("이 필드는 필수 항목입니다.", str(response.data["description"]))
