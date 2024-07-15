from django.test import SimpleTestCase
from django.core.exceptions import ValidationError


class EmailValidatorTestCase(SimpleTestCase):
    def setUpTestData(self): ...

    def test_validate_success_with_valid_emails(self): ...

    def test_validate_fail_with_too_long_emails(self): ...
