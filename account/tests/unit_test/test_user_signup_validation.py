from django.test import SimpleTestCase, TestCase
from rest_framework import serializers
from account.serializers import UserSignUpSerializer


class UserSignUpValidationTestCase(TestCase):
    def setUp(self):
        self.serializer = UserSignUpSerializer()

    def create_valid_data(self):
        return {"email": "test@email.com", "password": "SecurePass123"}

    def test_valid_data(self):
        # Given
        data = self.create_valid_data()

        # When
        serializer = UserSignUpSerializer(data=data)
        is_valid = serializer.is_valid()

        # Then
        self.assertTrue(is_valid)

    def test_invalid_email(self):
        # Given
        data = self.create_valid_data()
        data["email"] = "invalid-email"

        # When
        serializer = UserSignUpSerializer(data=data)
        is_valid = serializer.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn("email", serializer.errors)

    def test_password_too_short(self):
        # Given
        data = self.create_valid_data()
        data["password"] = "short"

        # When
        serializer = UserSignUpSerializer(data=data)
        is_valid = serializer.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn("password", serializer.errors)

    def test_email_length_limit(self):
        # Given
        data = self.create_valid_data()
        data["email"] = "a" * 246 + "@example.com"  # 256 characters

        # When
        serializer = UserSignUpSerializer(data=data)
        is_valid = serializer.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn("email", serializer.errors)

    def test_password_length_limit(self):
        # Given
        data = self.create_valid_data()
        data["password"] = "a" * 129  # Assuming max length is 128

        # When
        serializer = UserSignUpSerializer(data=data)
        is_valid = serializer.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn("password", serializer.errors)

    def test_email_without_at_symbol(self):
        # Given
        data = self.create_valid_data()
        data["email"] = "testexample.com"

        # When
        serializer = UserSignUpSerializer(data=data)
        is_valid = serializer.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn("email", serializer.errors)

    def test_email_with_multiple_at_symbols(self):
        # Given
        data = self.create_valid_data()
        data["email"] = "test@example@com"

        # When
        serializer = UserSignUpSerializer(data=data)
        is_valid = serializer.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn("email", serializer.errors)

    def test_password_without_uppercase(self):
        # Given
        data = self.create_valid_data()
        data["password"] = "securepass123"

        # When
        serializer = UserSignUpSerializer(data=data)
        is_valid = serializer.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn("password", serializer.errors)

    def test_password_without_lowercase(self):
        # Given
        data = self.create_valid_data()
        data["password"] = "SECUREPASS123"

        # When
        serializer = UserSignUpSerializer(data=data)
        is_valid = serializer.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn("password", serializer.errors)

    def test_password_without_number(self):
        # Given
        data = self.create_valid_data()
        data["password"] = "SecurePassword"

        # When
        serializer = UserSignUpSerializer(data=data)
        is_valid = serializer.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn("password", serializer.errors)

    def test_email_with_invalid_characters(self):
        # Given
        data = self.create_valid_data()
        data["email"] = "test!@example.com"

        # When
        serializer = UserSignUpSerializer(data=data)
        is_valid = serializer.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn("email", serializer.errors)

    def test_password_with_spaces(self):
        # Given
        data = self.create_valid_data()
        data["password"] = "Secure Pass 123"

        # When
        serializer = UserSignUpSerializer(data=data)
        is_valid = serializer.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn("password", serializer.errors)
