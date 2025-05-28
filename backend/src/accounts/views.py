from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from accounts.serializers import RegistrationSerializer, ConfirmCodeSerializer
from accounts.utils import set_jwt_token
from accounts.models import CustomUser
from accounts.services import register_user, confirm_code


class LoginView(TokenObtainPairView):
    """
    Хранение токена в HttpOnly
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            if access_token and refresh_token:
                response = set_jwt_token(
                    response=response,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )
                # Удаляем токены из тела ответа
                del response.data["access"]
                del response.data["refresh"]

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.data["refresh"] = refresh_token

        try:
            response = super().post(request, *args, **kwargs)

            if response.status_code == status.HTTP_200_OK:
                new_access_token = response.data.get("access")

                if new_access_token:
                    response = set_jwt_token(
                        response=response, access_token=new_access_token
                    )
                    del response.data["access"]

            return response

        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User does not exist"}, status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomTokenBlacklistView(TokenBlacklistView):
    """
    Выход из системы и очистка куков
    """

    def post(self, request, *args, **kwargs):
        # Получаем refresh токен из куки (Потому что фронтенд не должен передавать вручную)
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Добавляем refresh-токен в данные запроса
        request.data.update({"refresh": refresh_token})

        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            # Удаляем куки с токенами
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")

        return response


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        register_user(serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class ConfirmCodeView(APIView):
    serializer_class = ConfirmCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        confirm_code(serializer.validated_data)

        return Response(status=status.HTTP_200_OK)
