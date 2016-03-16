from __future__ import unicode_literals

from django.contrib.auth.models import User

from jsonfield2.managers import models, JSONAwareManager as Manager
from jsonfield2 import JSONField

from workspace.models import Workspace
# Create your models here.


class Api(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    request_host = models.CharField(max_length=255, null=False,
                                    blank=False, verbose_name='host')
    strip_request_path = models.BooleanField(default=False)
    preserve_host = models.BooleanField(default=False)
    upstream_url = models.URLField(verbose_name="url")
    creator = models.ForeignKey(User, related_name='apis')
    workspace = models.ForeignKey(Workspace, related_name='apis')
    active = models.BooleanField(default=True)
    login_required = models.BooleanField(default=False)

    manager = Manager

    class Meta:
        verbose_name = "Api"
        verbose_name_plural = "Apis"

    def __str__(self):
        self.name

    def __unicode__(self):
        self.name


class Endpoint(models.Model):
    request_path = models.CharField(max_length=255, blank=False, null=False,
                                    verbose_name='path')
    active = models.BooleanField(default=True)
    schema = JSONField()
    api = models.ForeignKey(Api, related_name='endpoints')

    class Meta:
        verbose_name = "Endpoint"
        verbose_name_plural = "Endpoints"

    def __str__(self):
        self.name

    def __unicode__(self):
        self.name
