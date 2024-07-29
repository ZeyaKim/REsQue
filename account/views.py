from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from account.serializers import UserSignUpSerializer, UserSignInSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSignUpSerializer


class SignInView(APIView):
    def post(self, request):

        serializer = UserSignInSerializer(data=request.data)
        print(f"request.data: {request.data}\nis_valid: {serializer.is_valid()}")

        if serializer.is_valid():
            email = serializer.validated_data["email"].strip()
            password = serializer.validated_data["password"]

            try:
                user = User.objects.get(email=email)

                if not user.is_active:
                    return Response(
                        {"error": "User account is disabled"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        },
                        status=status.HTTP_200_OK,
                    )
            except User.DoesNotExist:
                pass

            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
