from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import (authenticate, login as django_login,
                                 logout as django_logout)

from django.contrib.auth.models import User

from tastypie import fields
from tastypie.cache import SimpleCache
from tastypie.http import (HttpUnauthorized, HttpForbidden, HttpBadRequest,
                           HttpCreated)
from tastypie.utils import trailing_slash


from tastypie.resources import (ModelResource,)
from tastypie.validation import Validation
from tastypie.throttle import CacheDBThrottle
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import (SessionAuthentication,
                                     MultiAuthentication, ApiKeyAuthentication
                                     )

from app.models import Billing
from app.exceptions import CustomBadRequest
from workspace.models import (Organisation, Workspace, Invitation)


try:
    import json
except Exception:
    import simplejson as json

Authentication = MultiAuthentication(ApiKeyAuthentication(),
                                     SessionAuthentication(),)


class Resource(ModelResource):
    """docstring for Resource"""
    class Meta:

        always_return_data = True
        allowed_methods = ['get', 'post', 'put', 'patch', 'options', 'head']

        authentication = Authentication
        authorization = DjangoAuthorization()
        validation = Validation()
        collection_name = 'data'
        cache = SimpleCache(timeout=10)
        throttle = CacheDBThrottle(throttle_at=settings.THROTTLE_TIMEOUT)


class OrganisationResource(Resource):
    logo = fields.FileField()
    creator = fields.ToOneField('app.api.UserResource', 'creator')
    owner = fields.ToOneField('app.api.UserResource', 'owner')

    class Meta(Resource.Meta):
        queryset = Organisation.objects.filter(is_deleted=False)
        fields = ['id', 'name', 'logo', 'plan',
                  'slug', 'url', 'creator', 'owner']
        resource_name = 'orgs'


class BillingResource(Resource):
    class Meta(Resource.Meta):
        queryset = Billing.objects.all()
        resource_name = 'payments'


class UserResource(Resource):
    orgs_created = fields.ToManyField(
        OrganisationResource, blank=True, null=True,
        full=True, use_in='detail',
        attribute=lambda bundle: Organisation.objects
        .filter(creator=bundle.obj))
    orgs_owned = fields.ToManyField(
        OrganisationResource, blank=True, null=True,
        full=True, use_in='detail',
        attribute=lambda bundle: Organisation.objects.filter(owner=bundle.obj))
    orgs = fields.DictField(use_in='detail')

    class Meta(Resource.Meta):
        queryset = User.objects.all()
        fields = ['first_name', 'last_name',
                  'email', 'is_active', 'bills', 'orgs']
        resource_name = 'users'

    def dehydrate_orgs(self, bundle):
        created = bundle.data.pop('orgs_created')
        owned = bundle.data.pop('orgs_owned')
        orgs = {}

        orgs.update(owned=owned, created=created)
        return orgs

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def post_list(self, request, **kwargs):
        REQUIRED_USER_FIELDS = (
            "email", "password", "org", "first_name", "source")

        bundle = json.loads(request.body)

        for field in REQUIRED_USER_FIELDS:
            if field not in bundle:
                raise CustomBadRequest(
                    success=False,
                    code="missing_key",
                    message="Must provide %s when "
                    "creating a user." % field)

        REQUIRED_ORG_FIELDS = ("name", "url")

        for field in REQUIRED_ORG_FIELDS:
            if field not in bundle['org']:
                raise CustomBadRequest(
                    success=False,
                    code="missing_key",
                    message="Must provide %s when "
                    "creating an Organisation." % field)

        try:
            email = bundle["email"]
            org = bundle.pop('org')
            source = bundle.pop('source')

            if User.objects.filter(email=email):
                raise CustomBadRequest(
                    success=False,
                    code="duplicate_exception",
                    message="That email address is already in used.")
            if Organisation.objects.filter(url=org['url']):

                raise CustomBadRequest(
                    code="duplicate_exception",
                    message="The Organisation you are "
                    "trying to create already exist.")

            user = User.objects.create_user(username=email, **bundle)
            user = authenticate(username=user.email,
                                password=bundle['password'])

            if user:
                django_login(request, user)

                org.update(creator=user, owner=user)

                Organisation.objects.create(**org)

                auth = request.COOKIES

                if user.is_active:
                    data = {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'last_login': user.last_login
                    }

                    resp = {
                        'success': True,
                        'message': 'User created successfully',
                        'data': data,
                        'auth': auth
                    }
                    return self.create_response(request, resp, HttpCreated)

        except KeyError:
            raise CustomBadRequest()

    def login(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body,
                                format=request.META.get(
                                    'CONTENT_TYPE', 'application/json'))

        email = data.get('email', '')
        password = data.get('password', '')
        try:
            user = authenticate(username=email, password=password)
            if user:
                django_login(request, user)
                auth = request.COOKIES
                auth.update(apikey=user.api_key.key)
                if user.is_active:
                    data = {
                        'id': user.pk,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'last_login': user.last_login
                    }
                    resp = {
                        'success': True,
                        'message': 'Logged in successfully',
                        'data': data,
                        'auth': auth
                    }
                    return self.create_response(request, resp)
                else:
                    return self.create_response(request, {
                        'success': False,
                        'message': 'Your account have being suspended.',
                    }, HttpForbidden)
            else:
                raise CustomBadRequest(
                    code='invalid_entry',
                    message='Incorrect username/password combination.'
                )
        except KeyError:
            raise CustomBadRequest(
                code='invalid_entry',
                message='Incorrect username/password combination.'
            )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            django_logout(request)
            return self.create_response(request, {'success': True})
        else:
            raise CustomBadRequest(code='invalid_request',
                                   message="You are not logged in.")
