from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

class CustomEmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None 
        if user.is_verified == True:
            if user.check_password(password):
                return user  
            else:
                return None
        else:
            return Response({'msg':{'Your email is not verified'}}, status=status.HTTP_400_BAD_REQUEST)  
    def get_user(self, user_id):
        UserModel = get_user_model()

        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        
    def authenticate_header(self, request):
        """
        Returns a string to be used as the value of the WWW-Authenticate
        header in a HTTP 401 Unauthorized response.
        """
        return 'CustomEmailBackend realm="api"'