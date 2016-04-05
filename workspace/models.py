from __future__ import unicode_literals
import os

from datetime import datetime

import tldextract

from django.conf import settings
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User, Group

from panda.utils import random_string


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
    logo = models.ImageField(upload_to='organisations', null=True, blank=True)
    plan = models.CharField(
        verbose_name=_("Plan"), max_length=16, choices=PLANS,
        default=FREE,
        help_text=_("What plan your organization is on"))
    date_created = models.DateTimeField(
        verbose_name=_("Plan Start"), auto_now_add=True,
        help_text=_("When the user switched to this plan"))
    slug = models.SlugField(
        verbose_name=_("Slug"), max_length=255, null=True,
        blank=True, unique=True,
        error_messages=dict(unique=_("This slug is not available")))
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"
        unique_together = (('name', 'url'),)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def delete(self):
        if not self.is_deleted:
            self.is_deleted = True

        return self

    def save(self, *args, **kwargs):

        if not self.slug:
            tld = tldextract.extract(self.url)
            slug = slugify(tld.domain.lower() + tld.subdomain.lower())

            while Organisation.objects.filter(slug=slug):
                key = (random_string(3)).lower()
                slug = slugify((slug + key).lower())

            self.slug = slug
        if not self.logo:
            logo = reverse("django_pydenticon:image",
                           kwargs={"data": self.slug})
            self.logo = logo

        return super(Organisation, self).save(*args, **kwargs)


class OrganisationMember(models.Model):
    org = models.ForeignKey(Organisation, related_name='members')
    member = models.ForeignKey(User, related_name='orgs')

    class Meta:
        verbose_name = "OrganisationMember"
        verbose_name_plural = "OrganisationMembers"
        unique_together = (('org', 'member'),)

    def __str__(self):
        return "%s:%s" % (self.org, self.member)

    def __unicode__(self):
        return "%s:%s" % (self.org, self.member)


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
    key = models.CharField(
        max_length=255, blank=False, null=False, unique=True)
    accepted = models.BooleanField(default=False)
    creator = models.ForeignKey(User, related_name='invitations_created')
    role = models.ForeignKey(Group, related_name='invitations')
    org = models.ForeignKey(Organisation, related_name='invitations')
    expires_on = models.DateTimeField()

    class Meta:
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
        unique_together = (
            ('org', 'expires_on'),)

    def __str__(self):
        return self.key

    def __unicode__(self):
        return self.key

    def is_expired(self):
        return datetime.now() > self.expires_on

    def save(self, *args, **kwargs):

        if not self.key:
            key = random_string(32)

            while Invitation.objects.filter(key=key):
                key = random_string(32)

            self.key = key

        return super(Invitation, self).save(*args, **kwargs)

    @classmethod
    def generate_random_string(cls, length):
        """
        Generates a [length] characters alpha numeric secret
        """
        return random_string(length)
