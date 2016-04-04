"""panda URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView

import django_pydenticon.urls
from panda.urls.api import urlpatterns as patterns

urlpatterns = patterns + (
    url(r'^home/$',
        TemplateView.as_view(template_name='common/home.html'), name="home"),
    url(r'^hubs/$',
        TemplateView.as_view(template_name='common/hubs.html'), name="hubs"),
    url(r'^login/$',
        TemplateView.as_view(template_name='common/login.html'), name="login"),
    url(r'^register/$',
        TemplateView.as_view(template_name='common/register.html'),
        name="register"),
    url(r'^reset/$',
        TemplateView.as_view(template_name='common/reset.html'),
        name="reset"),




    url(r'^dashboard/$',
        TemplateView.as_view(template_name='account/home.html'),
        name="dashboard"),
    url(r'^hub/$',
        TemplateView.as_view(template_name='account/hubs.html'),
        name="hub"),
    url(r'^orgs/$',
        TemplateView.as_view(template_name='account/orgs.html'),
        name="orgs"),
    url(r'^workspaces/$',
        TemplateView.as_view(template_name='account/workspace.html'),
        name="workspace"),
    url(r'^plugins/$',
        TemplateView.as_view(template_name='account/plugins.html'),
        name="plugins"),
    url(r'^profile/$',
        TemplateView.as_view(template_name='account/profile.html'),
        name="profile"),




    url(r'^identicon/', include(django_pydenticon.urls.get_patterns())),

    url(r'^$', TemplateView.as_view(
        template_name='index.html')),

    url(r'^',
        TemplateView.as_view(template_name='index.html')),
)
