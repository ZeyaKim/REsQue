from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.validators import SignUpValidator

User = get_user_model()


class CustomUserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        super().validate(attrs)
        SignUpValidator.validate(attrs)
        return attrs
