from django.urls import path
from accounts.views import (
    CustomTokenObtainPairView,
    UserRegistrationAPIView,
    CustomTokenRefreshView,
    CustomTokenBlacklistView,
    UserConfirmCode,
)

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", CustomTokenBlacklistView.as_view(), name="logout"),
    path("confirm_code/", UserConfirmCode.as_view(), name="confirm_code"),
]
