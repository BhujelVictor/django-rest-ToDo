from django.urls import path
from accounts.views import *
urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(), name='register-user'),
    path('api/login/', UserLoginView.as_view(), name='login-user'),
    path('api/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/resend-code/', ResendVerificationCodeView.as_view(), name='resend-code')
]

