# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
        # URL pattern for the UserUpdateView
        url(
            regex=r'^~update/$',
            view=views.UserUpdateView.as_view(),
            name='update'
        ),
        )
