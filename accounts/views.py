from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.serializers import *
from django.contrib.auth import authenticate
from django.core.mail import send_mail
import random

def generate_otp():
    otp_code = str(random.randint(100000, 999999))
    return otp_code

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():   
            user = serializer.save()
            #Generate otp and save it
            otp = generate_otp()
            user.save()
            OTP.objects.create(user=user, otp=otp)
            # Send an email with the verification code
            subject = 'Activate your account'
            message = f'Your verification code is: {otp}'
            from_email = 'admin@gmail.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return Response({'msg':'User registered successfully. OTP has been sent to your email for verification.'}, status=status.HTTP_201_CREATED)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        else:
            raise serializers.ValidationError(serializer.errors)
        
class VerifyEmailView(APIView):
     def post(self, request, format=None):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'msg':'Your email has been verified.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendVerificationCodeView(APIView):
    def post(self, request, format=None):
        serializer = ResendVerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'msg': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            if user.is_verified:
                return Response({'msg': 'User is already verified'}, status=status.HTTP_400_BAD_REQUEST)

            otp = str(random.randint(100000, 999999))
            OTP.otp_created_at = timezone.now()
            OTP.objects.create(user=user, otp=otp)

            # Resend an email with the new verification code
            subject = 'Resend Verification Code'
            message = f'Your new verification code is: {otp}'
            from_email = 'admin@gmail.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return Response({'msg': 'New OTP for verification has been sent'}, status=status.HTTP_200_OK)

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