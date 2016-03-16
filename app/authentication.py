from tastypie.authentication import Authentication


class BaseAuth(Authentication):
    """docstring for BaseAuth"""

    def is_authenticated(self, request, **kwargs):
        if 'daniel' in request.user.username:
            return True

        return False
