from django.urls import path
from accounts.views import (
    LoginView,
    RegistrationView,
    CustomTokenRefreshView,
    CustomTokenBlacklistView,
    ConfirmCodeView,
)

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", CustomTokenBlacklistView.as_view(), name="logout"),
    path("confirm_code/", ConfirmCodeView.as_view(), name="confirm_code"),
]
