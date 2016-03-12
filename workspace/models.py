from __future__ import unicode_literals

from datetime import datetime

from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.contrib.auth.models import User, Group

FREE = 'FREE'
TIER1 = 'TIER1'
TIER2 = 'TIER2'

PLANS = (
    (FREE, _('Free Plan')),
    (TIER1, _('Pro Plan')),
    (TIER2, _('Special Plan'))
)


class Organisation(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    url = models.URLField(blank=False, null=False, max_length=255)
    creator = models.ForeignKey(User, related_name='orgs_created')
    owner = models.ForeignKey(User, related_name='orgs_owned')
    plan = models.CharField(
        verbose_name=_("Plan"), max_length=16, choices=PLANS,
        default=FREE,
        help_text=_("What plan your organization is on"))
    plan_start = models.DateTimeField(
        verbose_name=_("Plan Start"), auto_now_add=True,
        help_text=_("When the user switched to this plan"))
    slug = models.SlugField(
        verbose_name=_("Slug"), max_length=255, null=True,
        blank=True, unique=True,
        error_messages=dict(unique=_("This slug is not available")))

    class Meta:
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"
        unique_together = (('name', 'url'),)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Workspace(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    creator = models.ForeignKey(User, related_name='workspaces_created')
    owner = models.ForeignKey(User, related_name='workspaces_owned')
    org = models.ForeignKey(Organisation, related_name='workspaces')

    class Meta:
        verbose_name = "Workspace"
        verbose_name_plural = "Workspaces"
        unique_together = (('name', 'org'),)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Invitation(models.Model):
    email = models.EmailField(max_length=255, blank=False, null=False)
    key = models.CharField(max_length=255, blank=False, null=False)
    creator = models.ForeignKey(User, related_name='invitations_created')
    role = models.ForeignKey(Group, related_name='invitation')
    org = models.ForeignKey(Organisation, related_name='invitations')
    expires_on = models.DateTimeField()

    class Meta:
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
        unique_together = (('key', 'org', 'expires_on'),)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def is_expired(self):
        return datetime.now() > self.expires_on
