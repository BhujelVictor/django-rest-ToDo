from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class Backend(BaseBackend):
    def authenticate(username=None, password=None):
        UserModel = get_user_model()

        user_kwargs = {'email': username}


        try:
            user = UserModel.objects.get(**user_kwargs)
        except UserModel.DoesNotExist:
            return None  
        
        
        if user.check_password(password):
            return user 
        else:
            return None  

    def get_user(self, user_id):
        UserModel = get_user_model()

        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
