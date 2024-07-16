from django.core.exceptions import ValidationError


def validate_email_length(email: str, **kwargs): ...


class RegisterValidator:
    validate_funcs = [validate_email_length]

    @classmethod
    def validate(cls, kwargs):
        for validate_func in cls.validate_funcs:
            validate_func(**kwargs)
