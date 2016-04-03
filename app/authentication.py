"""
auth backends allowed us to use auth.authenticate.
taspiepie apikey & email authenticate support.
"""

from django.contrib.auth.models import User
from tastypie.authentication import Authentication


class ApiKeyBackend(Authentication):
    """
    username+api_key to authenticate
    """

    def authenticate(self, username=None, api_key=None):
        if not username or not api_key:
            return None
        try:
            return User.objects.get(username=username, api_key__key=api_key)
        except User.DoesNotExist:
            return None


class EmailBackend(Authentication):
    """
    email+password to authenticate
    """

    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
