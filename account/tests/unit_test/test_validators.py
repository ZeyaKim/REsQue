from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from account.validators import validate_email_length


class ValidatorTestCase(SimpleTestCase):
    def setUp(self): ...

    def test_raise_validation_error_when_email_is_too_long(self):
        # Arrange
        data = {
            "email": "dsfsdfsdfdsfsdfssfsdfdsfsdfsfsfsdfdsfsdfsfsfsdfdsfsdfsfsfsdfdsfsdfsf@naver.com",
            "password": "jason1234",
        }

        # Act
        with self.assertRaises(ValidationError) as e:
            validate_email_length(**data)

        # Assert
        self.assertEqual(
            str(e.exception.message), "Ensure this value has at most 50 characters."
        )

    def test_pass_validation_email_within_max_length(self):
        # Arrange
        data = {
            "email": "dsfsdfsdfdsfsdfssff@naver.com",
            "password": "jason1234",
        }

        # Act
        try:
            validate_email_length(**data)
        except ValidationError:
            self.fail()
