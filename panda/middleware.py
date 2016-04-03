"""Summary."""

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import DisallowedHost
from django.db import connection


from tenant_schemas.utils import (get_tenant_model,
                                  get_public_schema_name)
from tenant_schemas.middleware import TenantMiddleware

from panda.utils import remove_www


class SubdomainMiddleware(TenantMiddleware):
    """Custom subdamain middleware.

    This middleware should be placed at the very top of the middleware stack.
    Selects the proper database schema using the request host. Can fail in
    various ways which is better than corrupting or revealing data.

    Attributes:
        TENANT_NOT_FOUND_EXCEPTION (TYPE): Description
    """

    TENANT_NOT_FOUND_EXCEPTION = DisallowedHost

    def hostname_from_request(self, request):
        """Extract hostname from request. Used for custom requests filtering.

        By default removes the request's port and common prefixes.

        Args:
            request (TYPE): Description
        """
        return remove_www(request.get_host().split(':')[0])

    def process_request(self, request):
        """
        Summary.

        Args:
            request (TYPE): Description

        Raises:
            self.TENANT_NOT_FOUND_EXCEPTION: Description

        Returns:
            name (TYPE): Description
        """
        # Connection needs first to be at the public schema, as this is where
        # the tenant metadata is stored.
        connection.set_schema_to_public()
        hostname, www = self.hostname_from_request(request)

        tenant_model = get_tenant_model()
        try:
            request.tenant = tenant_model.objects.get(domain_url=hostname)
            connection.set_tenant(request.tenant)
        except tenant_model.DoesNotExist:
            try:
                request.tenant = tenant_model.objects.get(domain_url=www)
                connection.set_tenant(request.tenant)
            except tenant_model.DoesNotExist:
                raise self.TENANT_NOT_FOUND_EXCEPTION(
                    'No tenant for hostname "%s"' % hostname)

        # Content type can no longer be cached as public and tenant schemas
        # have different models. If someone wants to change this, the cache
        # needs to be separated between public and shared schemas. If this
        # cache isn't cleared, this can cause permission problems. For example,
        # on public, a particular model has id 14, but on the tenants it has
        # the id 15. if 14 is cached instead of 15, the permissions for the
        # wrong model will be fetched.
        ContentType.objects.clear_cache()

        # Do we have a public-specific urlconf?
        if hasattr(settings,
                   'PUBLIC_SCHEMA_URLCONF') and request.tenant\
                .schema_name == get_public_schema_name():
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
