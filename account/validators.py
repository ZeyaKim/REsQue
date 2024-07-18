from django.core.exceptions import ValidationError
import re


def validate_email_length(email: str, **kwargs):
    if len(email) > 50:
        raise ValidationError("Ensure this value has at most 50 characters.")


def validate_password_contains_digit(password: str, **kwargs):
    if not any(ch.isdigit() for ch in password):
        raise ValidationError("Password must contain at least one digit.")


def validate_password_contains_letter(password: str, **kwargs):
    if not any(ch.isalpha() for ch in password):
        raise ValidationError("Password must contain at least one letter.")


class SignUpValidator:
    validate_funcs = [validate_email_length]

    @classmethod
    def validate(cls, kwargs):
        for validate_func in cls.validate_funcs:
            validate_func(**kwargs)
