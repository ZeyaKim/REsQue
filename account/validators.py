from django.core.exceptions import ValidationError


def validate_email_length(email: str, **kwargs):
    if len(email) > 50:
        raise ValidationError("Ensure this value has at most 50 characters.")


class RegisterValidator:
    validate_funcs = [validate_email_length]

    @classmethod
    def validate(cls, kwargs):
        for validate_func in cls.validate_funcs:
            validate_func(**kwargs)
