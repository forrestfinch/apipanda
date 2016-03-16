from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.utils import trailing_slash

from tastypie.resources import (ModelResource,)
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import (SessionAuthentication,
                                     MultiAuthentication, ApiKeyAuthentication
                                     )
from app.authentication import BaseAuth
from app.models import Billing

Authentication = MultiAuthentication(BaseAuth(), SessionAuthentication(),
                                     ApiKeyAuthentication(),)


class BillingResource(ModelResource):
    class Meta:
        queryset = Billing.objects.all()
        resource_name = 'payment'

        always_return_data = True

        authentication = Authentication
        authorization = DjangoAuthorization()


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        fields = ['first_name', 'last_name', 'email', 'is_active', 'bills']
        allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
        resource_name = 'users'

        always_return_data = True

        authentication = Authentication
        authorization = DjangoAuthorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get(
                                    'CONTENT_TYPE', 'application/json'))

        email = data.get('email', '')
        password = data.get('password', '')

        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False},
                                        HttpUnauthorized)
