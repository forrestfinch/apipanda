from django.contrib import admin
from workspace.admin import BaseAdmin

from endpoint.models import Api, Endpoint
# Register your models here.


class OrganisationAdmin(BaseAdmin):
    '''
        Admin View for Organisation
    '''
    date_hierarchy = 'date_created'
    readonly_fields = ('creator', 'plan')
    exclude = ('slug',)
    list_display = ('name', 'plan', 'owner', 'date_created')
    list_filter = ('name', 'plan', 'date_created')
    search_fields = ('owner__username', 'plan', 'name')


class ApiAdmin(BaseAdmin):
    '''
        Admin View for Endpoint
    '''
    list_display = ('name', 'request_host', 'creator',
                    'workspace', 'login_required')
    list_filter = ('creator', 'workspace', 'login_required')
    search_fields = ('name', 'request_host')


class EndpointAdmin(BaseAdmin):
    '''
        Admin View for Endpoint
    '''
    list_display = ('request_path', 'active', 'api')
    list_filter = ('active', 'api')
    search_fields = ('request_path', 'api')

admin.site.register(Api, ApiAdmin)
admin.site.register(Endpoint, EndpointAdmin)
