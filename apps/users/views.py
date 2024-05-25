from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import send_activation_email
from .serializers import (
    UserRegistrationSerializer, ResendActivationEmailSerializer,
    UserLoginSerializer, LogoutSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Обработка регистрации пользователя.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_activation_email(user, request)
            return Response({
                'message': (
                    'Registration successful. '
                    'Please check your email to confirm your account.'
                )},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, uid, token):
        """
        Обработка активации аккаунта по ссылке из письма.
        """
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_email_verified = True
                user.save()
                return render(request, 'users/activation_success.html')
            else:
                return render(request, 'users/activation_failed.html')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(request, 'users/activation_failed.html')


class ResendActivationEmailView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Обработка повторной отправки активационного письма.
        """
        serializer = ResendActivationEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                if user and not user.is_email_verified:
                    send_activation_email(user, request)
                    return Response({
                        'message': 'Activation email sent'},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response({
                        'message': 'Email is already verified or not exist'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except User.DoesNotExist:
                return Response({
                    'message': 'User with this email does not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Обработка входа пользователя.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_email_verified:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token), },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'message': 'Email is not verified'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            return Response(
                {'message': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Обработка выхода пользователя.
        """
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data.get('refresh')
            blacklist = serializer.validated_data.get('blacklist', False)

            if refresh_token and blacklist:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionExpiredView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Отображение страницы истекшей сессии.
        """
        return render(request, 'users/session_expired.html')
