from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from account.serializers import CustomUserSignUpSerializer


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSignUpSerializer
