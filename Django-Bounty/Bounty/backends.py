from django.contrib.auth.backends import ModelBackend
from .models import AdminUser, PublisherUser

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, telephone=None, password=None, user_type=None):
        if user_type == 'admin':
            user = AdminUser.objects.filter(telephone=telephone).first()
            if user and user.check_password(password):
                return user
        elif user_type == 'publisher':
            user = PublisherUser.objects.filter(telephone=telephone).first()
            if user and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return AdminUser.objects.get(AccountID=user_id)
        except AdminUser.DoesNotExist:
            try:
                return PublisherUser.objects.get(AccountID=user_id)
            except PublisherUser.DoesNotExist:
                return None