from django.urls import path

from .views import DeactivationView, SignInView, SignUpView

urlpatterns = [
    path("user-signup/", SignUpView.as_view(), name="user-signup"),
    path("user-signin/", SignInView.as_view(), name="user-signin"),
    path("user-deactivation/", DeactivationView.as_view(), name="user-deactivation"),
]
