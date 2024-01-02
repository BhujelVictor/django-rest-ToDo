from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from accounts.models import User
from datetime import timedelta
from django.utils import timezone
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        # For confirm password field in Registration Request
        model = User
        fields = ['email','name','password','password2']
        extra_kwargs ={
            'password': {'write_only':True}
        }
    # password and confirm password2 validation
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class VerifyEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['otp', 'email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        OTP = attrs.get('otp')
        #Checking if email exists or not
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            otp_expiry_time = user.otp_created_at + timedelta(minutes=5)  
            #otp expires if it preceeds 5 min
            if timezone.now() > otp_expiry_time:
                raise serializers.ValidationError('OTP has expired')
            #verify otp
            if not user.otp == OTP :
                raise serializers.ValidationError('OTP does not match')
        else:
            raise serializers.ValidationError('Email does not exist')
        user.is_verified = True
        user.otp = None
        user.save()
        return attrs
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']

