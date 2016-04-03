from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from jsonfield2.managers import models, JSONAwareManager as Manager
from jsonfield2 import JSONField

from request.models import Request as Requests

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
        verbose_name = "API"
        verbose_name_plural = "APIs"

    def __str__(self):
        self.name

    def __unicode__(self):
        self.name


class Endpoint(models.Model):
    request_path = models.CharField(max_length=255, blank=False, null=False,
                                    verbose_name='path')
    active = models.BooleanField(default=True)
    schema = JSONField()
    api = models.ForeignKey(Api, related_name='apis')

    class Meta:
        verbose_name = "Endpoint"
        verbose_name_plural = "Endpoints"

    def __str__(self):
        self.request_path

    def __unicode__(self):
        self.request_path


class Request(Requests):

    meta = JSONField()
    client = models.ForeignKey(User, related_name='requests')
    endpoint = models.ForeignKey(Endpoint, related_name='requests')
    api = models.ForeignKey(Api, related_name='requests')

    def __unicode__(self):
        return '[%s] %s %s %s' % (self.time, self.method,
                                  self.path, self.response)
