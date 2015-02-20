# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# ajaxuploader
from ajaxuploader.views import AjaxFileUploader
uploader = AjaxFileUploader()

# Django-notifications
# import notifications


urlpatterns = patterns('',
    url(r'^$',  # noqa
        TemplateView.as_view(template_name='pages/home.html'),
        name="home"),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'),
        name="about"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^accounts/signup/$', LocalSignupView.as_view(), name='account_signup'),
    # User management
    url(r'^users/', include("users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # Uncomment the next line to enable avatars
    url(r'^avatar/', include('avatar.urls')),

    # Your stuff: custom urls go here
    url(r'^agent/', include("agent.urls", namespace="agent")),

    # Your stuff: custom urls go here
    url(r'^client/', include("clients.urls", namespace="clients")),

    # Django-ajax-ipload-widget urls
    (r'^ajax-upload/', include('ajax_upload.urls')),

    # Django-messages-extends urls
    (r'^messages/', include('messages_extends.urls')),

    # Django-plans
    url(r'^plan/', include('plans.urls',)),


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
