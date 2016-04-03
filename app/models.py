from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from tenant_schemas.models import TenantMixin

from workspace.models import Organisation
# Create your models here.


class Billing(models.Model):

    reference = models.CharField(blank=False, null=False, max_length=255)
    transaction_date = models.DateTimeField()
    domain = models.CharField(max_length=15)
    card_type = models.CharField(max_length=32)
    bank = models.CharField(max_length=255)
    card_digits = models.CharField(max_length=4)
    authorization_code = models.CharField(max_length=255,
                                          blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, related_name='bills')
    organisation = models.ForeignKey(Organisation, related_name='bills')

    class Meta:
        verbose_name = "Billing"
        verbose_name_plural = "Billings"
        unique_together = (('reference', 'authorization_code'),)

    def __str__(self):
        return "{0}:{1}".format(self.pk, self.reference)

    def ___unicode__(self):
        return "{0}:{1}".format(self.pk, self.reference)


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateTimeField(verbose_name='Expires On')
    on_trial = models.BooleanField(default=True)
    organisation = models.ForeignKey(Organisation, related_name="subdomain")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        unique_together = (('name', 'organisation'),)
