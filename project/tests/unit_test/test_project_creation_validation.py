from django.test import TestCase
from rest_framework.test import APIClient


class ProjectCreationValidationTestCase(TestCase):
    def setUp(self): ...

    def test_project_creation_with_valid_data(self): ...

    def test_project_creation_with_empty_title(self): ...

    def test_project_creation_with_too_long_title(self): ...

    def test_project_creation_with_too_long_description(self): ...

    def test_project_creation_with_missing_title(self): ...

    def test_project_creation_with_missing_description(self): ...

    def test_project_creation_with_non_string_title(self): ...

    def test_project_creation_with_non_string_description(self): ...
