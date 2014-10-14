# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    # URL pattern for the AgentDetailView
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.AgentDetailView.as_view(),
        name='details'
    ),
    # URL pattern for the AgentCreateView
    url(
        regex=r'^~create/$',
        view=views.AgentCreateView.as_view(),
        name='create'
    ),
    # URL pattern for the AgentCreateView
    url(
        regex=r'^~update/$',
        view=views.AgentUpdateView.as_view(),
        name='update'
    ),
    # URL pattern for the PoleEmploiCreateView
    url(
        regex=r'^~update_poleemploi/$',
        view=views.PoleEmploiUpdateView.as_view(),
        name='update_poleemploi'
    ),
    # URL pattern for the AgentCertificationsCreateView
    url(
        regex=r'^~create_agentcertifications/$',
        view=views.AgentCertificationsCreateView.as_view(),
        name='create_agentcertifications'
    ),
)
