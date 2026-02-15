from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework.views import APIView
from users.authentication import CookieJWTAuthentication

from .models import *
from .serializer import *
from .utils import set_jwt_cookies, clear_jwt_cookies

class RegisterView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        response = Response(
            {"detail": "Registration successful"},
            status=status.HTTP_201_CREATED,
        )

        set_jwt_cookies(
            response,
            access=str(refresh.access_token),
            refresh=str(refresh),
        )

        return response

class LoginView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=email, password=password)

        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        response = Response(
            {"detail": "Login successful"},
            status=status.HTTP_200_OK,
        )

        set_jwt_cookies(
            response,
            access=str(refresh.access_token),
            refresh=str(refresh),
        )

        return response

class LogoutView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmptySerializer

    def post(self, request):
        response = Response(
            {"detail": "Logged out"},
            status=status.HTTP_200_OK,
        )
        clear_jwt_cookies(response)
        return response


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = (
            request.data.get("refresh")
            or request.COOKIES.get("refresh")
        )

        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data["refresh"] = refresh_token

        request._full_data = data

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            set_jwt_cookies(
                response,
                access=response.data.get("access"),
                refresh=response.data.get("refresh"),
            )

        return response

class ProfileView(RetrieveUpdateAPIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)