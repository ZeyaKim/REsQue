from django.test import SimpleTestCase
from project.serializers import ProjectSerializer


class ProjectCreationValidationTestCase(SimpleTestCase):
    def setUp(self):
        pass

    def create_valid_project_data(self):
        return {
            "title": "Test Project",
            "description": "This is a test project.",
        }

    def test_project_creation_with_valid_data(self):
        # Given
        valid_project_data = self.create_valid_project_data()

        # When
        project_serializer = ProjectSerializer(data=valid_project_data)

        # Then
        self.assertTrue(project_serializer.is_valid())

    def test_project_creation_with_empty_title(self):
        # Given
        invalid_project_data = self.create_valid_project_data()
        invalid_project_data["title"] = ""

        # When
        project_serializer = ProjectSerializer(data=invalid_project_data)

        # Then
        self.assertFalse(project_serializer.is_valid())
        self.assertEqual(
            project_serializer.errors["title"][0], "이 필드는 blank일 수 없습니다."
        )

    def test_project_creation_with_too_long_title(self):
        # Given
        invalid_project_data = self.create_valid_project_data()
        invalid_project_data["title"] = "a" * 101

        # When
        project_serializer = ProjectSerializer(data=invalid_project_data)

        # Then
        self.assertFalse(project_serializer.is_valid())
        self.assertEqual(
            project_serializer.errors["title"][0],
            "이 필드의 글자 수가 100 이하인지 확인하십시오.",
        )

    def test_project_creation_with_too_long_description(self):
        # Given
        invalid_project_data = self.create_valid_project_data()
        invalid_project_data["description"] = "a" * 1001

        # When
        project_serializer = ProjectSerializer(data=invalid_project_data)

        # Then
        self.assertFalse(project_serializer.is_valid())
        self.assertEqual(
            project_serializer.errors["description"][0],
            "이 필드의 글자 수가 1000 이하인지 확인하십시오.",
        )

    def test_project_creation_with_missing_title(self):
        # Given
        invalid_project_data = self.create_valid_project_data()
        del invalid_project_data["title"]

        # When
        project_serializer = ProjectSerializer(data=invalid_project_data)

        # Then
        self.assertFalse(project_serializer.is_valid())
        self.assertEqual(
            project_serializer.errors["title"][0], "이 필드는 필수 항목입니다."
        )

    def test_project_creation_with_missing_description(self):
        # Given
        invalid_project_data = self.create_valid_project_data()
        del invalid_project_data["description"]

        # When
        project_serializer = ProjectSerializer(data=invalid_project_data)

        # Then
        self.assertFalse(project_serializer.is_valid())
        self.assertEqual(
            project_serializer.errors["description"][0], "이 필드는 필수 항목입니다."
        )

    def test_project_creation_with_non_string_title(self):
        # Given
        invalid_project_data = self.create_valid_project_data()
        invalid_project_data["title"] = 123

        # When
        project_serializer = ProjectSerializer(data=invalid_project_data)

        # Then
        self.assertFalse(project_serializer.is_valid())
        self.assertEqual(
            project_serializer.errors["title"][0], "이 필드는 문자열이어야 합니다."
        )

    def test_project_creation_with_non_string_description(self):
        # Given
        invalid_project_data = self.create_valid_project_data()
        invalid_project_data["description"] = 123

        # When
        project_serializer = ProjectSerializer(data=invalid_project_data)

        # Then
        self.assertFalse(project_serializer.is_valid())

        self.assertEqual(
            project_serializer.errors["description"][0],
            "이 필드는 문자열이어야 합니다.",
        )
