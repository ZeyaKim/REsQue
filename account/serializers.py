import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        return data

    def validate_email(self, value):
        errors = []

        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(email_pattern, value):
            errors.append("Invalid email format")

        if any(invalid_char in value for invalid_char in "!#$%^&*()=+[]';,/{}|\":<>?"):
            errors.append("Invalid character in email")

        if "@" not in value:
            errors.append("Email must contain @ symbol")

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def validate_password(self, value):
        errors = []

        if not any(char.islower() for char in value):
            errors.append("Password must contain at least one lowercase letter")

        if not any(char.isupper() for char in value):
            errors.append("Password must contain at least one uppercase letter")

        if not any(char.isdigit() for char in value):
            errors.append("Password must contain at least one digit")

        if " " in value:
            errors.append("Password must not contain spaces")

        if not 5 < len(value) < 31:
            errors.append("Password must be between 6 and 30 characters long")

        if errors:
            raise serializers.ValidationError(errors)

        return value


class UserSignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password")
            if not user.is_active:
                raise serializers.ValidationError("User is inactive")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'")

        return data
