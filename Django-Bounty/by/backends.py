from django.contrib.auth.backends import BaseBackend
from .models import Admin, Publisher

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, telephone=None, password=None, user_type=None):
        user_model = None
        if user_type == 'admin':
            user_model = Admin
        elif user_type == 'publisher':
            user_model = Publisher
        else:
            return None

        try:
            user = user_model.objects.get(telephone=telephone)
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        user_models = [Admin, Publisher]
        for user_model in user_models:
            try:
                return user_model.objects.get(AccountID=user_id)
            except user_model.DoesNotExist:
                continue
        return None