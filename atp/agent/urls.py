# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    # URL pattern for the AgentCreateView
    url(
        regex=r'^~agent/$',
        view=views.AgentView.as_view(),
        name='~agent'
    ),
    # URL pattern for the AgentCertificationsCreateView
    url(
        regex=r'^~agent_certification/$',
        view=views.AgentCertificationsCreateView.as_view(),
        name='~agent_certification'
    ),
    # URL pattern for the AgentIdCard
    url(
        regex=r'^~agent_id_card/$',
        view=views.AgentIdCardView.as_view(),
        name='~agent_id_card'
    ),
    # URL pattern for the AgentIdCard
    url(
        regex=r'^~agent_address/$',
        view=views.AgentAddressView.as_view(),
        name='~agent_address'
    ),
    # URL pattern for the AgentIdCard
    url(
        regex=r'^~agent_procard/$',
        view=views.AgentProCardView.as_view(),
        name='~agent_pro_card'
    ),
)
