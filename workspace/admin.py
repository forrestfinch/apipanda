from django.contrib import admin

from workspace.models import (Organisation, Workspace,
                              Invitation)
from app.models import (Billing, Client)
# Register your models here.


class BaseAdmin(admin.ModelAdmin):
    '''
        Admin View for Base
    '''

    actions_on_top = False
    actions_on_bottom = True
    empty_value_display = '-empty-'
    list_per_page = 50
    list_select_related = True
    save_as = True
    view_on_site = True

    # raw_id_fields = ('',)
    # search_fields = ('',)


class OrganisationAdmin(BaseAdmin):
    '''
        Admin View for Organisation
    '''
    date_hierarchy = 'date_created'
    readonly_fields = ('creator', 'plan')
    exclude = ('slug',)
    list_display = ('name', 'plan', 'owner', 'date_created')
    list_filter = ('plan', 'date_created')
    search_fields = ('owner__username', 'plan', 'name')


class WorkspaceAdmin(BaseAdmin):
    '''
        Admin View for Workspace
    '''
    list_display = ('name', 'org', 'owner', 'creator')
    list_filter = ('org', 'owner')

    readonly_fields = ('creator',)
    search_fields = ('name', 'org', 'owner')


class InvitationAdmin(BaseAdmin):
    '''
        Admin View for Invitation
    '''
    list_display = (
        'email', 'org', 'role', 'creator', 'expires_on', 'accepted')
    list_filter = ('org', 'role', 'expires_on', 'accepted')

    readonly_fields = ('key',)
    search_fields = ('org', 'expires_on', 'email', 'creator')


class ClientAdmin(BaseAdmin):
    '''
        Admin View for Invitation
    '''
    list_display = (
        'name', 'organisation', 'paid_until', 'on_trial')
    list_filter = ('paid_until', 'on_trial')

    readonly_fields = ('paid_until', 'organisation')
    search_fields = ('organisation', 'name')


class BillingAdmin(BaseAdmin):
    '''
        Admin View for Invitation
    '''
    list_display = (
        'reference', 'organisation', 'customer', 'transaction_date', 'domain')
    list_filter = ('customer', 'transaction_date')

    readonly_fields = ('reference', 'customer', 'transaction_date',
                       'card_digits', 'authorization_code', 'created_on',
                       'card_type', 'bank')
    search_fields = ('organisation', 'reference')

admin.site.register(Client, ClientAdmin)
admin.site.register(Billing, BillingAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Workspace, WorkspaceAdmin)
admin.site.register(Organisation, OrganisationAdmin)
