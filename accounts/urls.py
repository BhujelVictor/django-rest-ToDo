from django.urls import path
from accounts.views import *
urlpatterns = [
    path('api/register_user/', UserRegistrationView.as_view(), name='register-user'),
    path('api/login/', UserLoginView.as_view(), name='login-user'),
    path('api/logout/', UserLogoutView.as_view(), name='logout-user'),
    path('api/verify_email/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/resend_code/', ResendVerificationCodeView.as_view(), name='resend-code')
]

