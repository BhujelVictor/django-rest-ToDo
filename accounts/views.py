from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.serializers import *
from django.contrib.auth import authenticate
from accounts.utils import Util
from django.core.mail import send_mail

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():   
            user = serializer.save() # otp_created_at is created when this is saved
            user.otp = Util.generateOTP()
            user.save()
            # Send an email with the verification code
            subject = 'Activate your account'
            message = f'Your verification code is: {user.otp}'
            from_email = 'admin@gmail.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return Response({'msg':'OTP for verification has been sent'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmailView(APIView):
     def post(self, request, format=None):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'msg':'Your email has been verified.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = User.objects.get(email=email)
            if user.is_verified == True:
                user = authenticate(email=email,password=password)
            else:
                return Response({'msg':{'Your email is not verified'}}, status=status.HTTP_400_BAD_REQUEST)
            if user is not None:
                return Response({'msg':{'Login Success'}}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'Email or Password is not Valid'}}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)