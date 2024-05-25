from django.urls import path

from .views import (
    RegisterView, VerifyEmailView, LoginView,
    LogoutView, ResendActivationEmailView, SessionExpiredView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path(
        'resend-activation-email/',
        ResendActivationEmailView.as_view(),
        name='resend_activation_email'
    ),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'verify-email/<str:uid>/<str:token>/',
        VerifyEmailView.as_view(),
        name='verify-email'
    ),
    path(
        'session-expired/',
        SessionExpiredView.as_view(),
        name='session_expired'
    ),
]
