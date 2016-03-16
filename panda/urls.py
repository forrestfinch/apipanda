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
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from django.conf import settings

from tastypie.api import Api

from app import api

resource = Api(api_name=settings.TASTYPIE_API_VERSION)

resource.register(api.UserResource())

urlpatterns = [

    url(r'^api/', include(resource.urls)),
    url(r'^app/', TemplateView.as_view(template_name='home.html')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),

    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^control/', include(admin.site.urls)),
    url(r'^showconfig/', 'kong_admin.views.show_config'),
    url(r'ab/', include('experiments.urls')),

    # Everyother views redirects here
    # url(r'^', TemplateView.as_view(template_name='404.html')),
]
