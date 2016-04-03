"""Util functions."""
import random
from django.conf import settings


def remove_www(hostname):
    """
    Split www. from the beginning of the address.

    Only for routing purposes. www.test.com/login/ and test.com/login/ should
    find the same tenant.
    """
    restricted_subdomains = settings.SUBDOMAIN_URLCONFS.keys()

    hostname_parts = hostname.split('.')
    subdomain = hostname_parts[0]

    if subdomain in restricted_subdomains:
        return '.'.join(hostname_parts[1:]), subdomain

    return hostname, None


def random_string(length):
    """Generate a random alphanumeric string."""
    letters = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return ''.join([random.choice(letters) for _ in range(length)])
