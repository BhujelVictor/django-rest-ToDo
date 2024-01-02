from django.urls import path
from accounts.views import *
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register-user'),
    path('login/', UserLoginView.as_view(), name='login-user'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email')

]
