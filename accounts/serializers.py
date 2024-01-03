from rest_framework.response import Response
from rest_framework import serializers
from accounts.models import User, OTP
from datetime import timedelta
from django.utils import timezone

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('user', 'otp', 'otp_created_at')

class UserRegistrationSerializer(serializers.ModelSerializer):
    # For confirm password field in Registration Request
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email','name','password','confirm_password']
        # passed as write_only to prevent serialization of password for security, only to be used to avoid serialization of data
        extra_kwargs ={
            'password': {'write_only':True}
        }
    # password and confirm confirm_password validation
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class VerifyEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['otp', 'email']
    
    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        #Checking if email exists or not
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            #Checking for otp record
            try:
                otp_record = OTP.objects.get(user=user, otp=otp, otp_created_at__gte=timezone.now() - timedelta(minutes=5))
            except OTP.DoesNotExist:
                raise serializers.ValidationError('OTP does not match or has timed out')

            otp_record.delete()
            user.is_verified = True
            user.save()
            
        else:
            raise serializers.ValidationError('Email does not exist')
        
        return data
    
class ResendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email', 'otp']
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']

