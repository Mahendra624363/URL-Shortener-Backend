from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from .views import RegisterView, VerifyEmailView,ProfileView,CustomTokenObtainPairView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify/<uuid:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="token-blacklist"),
    path("profile/", ProfileView.as_view(), name="profile"),
]