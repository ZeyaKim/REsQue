from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from account import validators
from faker import Faker

fake = Faker()


class ValidatorTestCase(SimpleTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_email = fake.email()
        cls.valid_password = fake.password()

    def test_pass_validation(self):
        # Arrange
        data = {"email": self.valid_email, "password": self.valid_password}

        # Act & Assert
        try:
            validators.RegisterValidator.validate(data)
        except ValidationError:
            self.fail("RegisterValidator raised ValidationError unexpectedly.")

    def test_raise_validation_error_when_email_is_too_long(self):
        # Arrange
        data = {"email": "a" * 50 + self.valid_email, "password": self.valid_password}

        # Act & Assert
        with self.assertRaises(ValidationError) as e:
            validators.validate_email_length(**data)

        self.assertIn("Ensure this value has at most 50 characters.", str(e.exception))

    def test_raise_validation_error_when_password_composed_with_only_characters(self):
        # Arrange
        data = {"email": self.valid_email, "password": "jasonesdfs"}

        # Act & Assert
        with self.assertRaises(ValidationError) as e:
            validators.validate_password_contains_digit(**data)

        self.assertIn("Password must contain at least one digit.", str(e.exception))

    def test_raise_validation_error_when_password_composed_with_only_numbers(self):
        # Arrange
        data = {"email": self.valid_email, "password": "1234567890"}

        # Act & Assert
        with self.assertRaises(ValidationError) as e:
            validators.validate_password_contains_letter(**data)

        self.assertIn("Password must contain at least one letter.", str(e.exception))

    def test_raise_validation_error_when_password_is_too_short(self):
        # Arrange
        data = {"email": self.valid_email, "password": "12345"}

        # Act & Assert
        with self.assertRaises(ValidationError) as e:
            validators.validate_password_length(**data)

        self.assertIn("Password must contain at least 8 characters.", str(e.exception))
