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

    def validate_email(self, value):
        # 기본 이메일 형식 검증
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise serializers.ValidationError("Invalid email format.")

        # 길이 검증
        if len(value) > 254:
            raise serializers.ValidationError("Email must not exceed 254 characters.")

        # 공백 검사
        if " " in value:
            raise serializers.ValidationError("Email must not contain spaces.")

        # 추가적인 패턴 필터링
        local_part, domain = value.split("@")

        # 로컬 파트 검증
        if not re.match(r"^[a-zA-Z0-9._-]+$", local_part):
            raise serializers.ValidationError(
                "Email local part can only contain letters, numbers, dots, underscores and hyphens."
            )

        # 특정 특수 문자 제한 (예: '+' 문자 거부)
        if "+" in local_part:
            raise serializers.ValidationError("Email must not contain '+' character.")

        # 도메인 파트 검증
        if not re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", domain):
            raise serializers.ValidationError("Invalid email domain.")

        # 추가적인 도메인 제한 (예: 특정 도메인만 허용)
        allowed_domains = ["example.com", "yourdomain.com"]  # 허용할 도메인 목록
        if domain not in allowed_domains:
            raise serializers.ValidationError(
                f"Email domain not allowed. Allowed domains are: {', '.join(allowed_domains)}"
            )

        return value.lower()  # 이메일을 소문자로 정규화

    def validate_password(self, value):
        # 비밀번호 길이 검증
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )

        # 유니코드 문자 검사
        if any(ord(char) > 127 for char in value):
            raise serializers.ValidationError(
                "Password must not contain Unicode characters."
            )

        # 대문자, 소문자, 숫자 포함 여부 검증
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )

        return value

    def validate(self, data):
        if not all(data.values()):
            raise serializers.ValidationError("All fields are required.")
        return data
