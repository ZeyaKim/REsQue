from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from account.validators import validate_email_length


class RegisterValidatorTestCase(SimpleTestCase):
    def setUp(self): ...

    def test_validate_email_length(self):
        data = {
            "email": "dsfsdfsdfdsfsdfssfsdfdsfsdfsfsfsdfdsfsdfsfsfsdfdsfsdfsfsfsdfdsfsdfsf@naver.com",
            "password": "jason1234",
        }

        with self.assertRaises(ValidationError) as e:
            validate_email_length(data)

        self.assertEqual(
            str(e.exception) == "Ensure this value has at most 50 characters."
        )
