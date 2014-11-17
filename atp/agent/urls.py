# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

from .views import HelloPDFView

urlpatterns = patterns('',
    # URL pattern for the AgentHomeView
    url(
        regex=r'^~agent/home$',
        view=views.AgentHomeView.as_view(),
        name='~agent_home'
    ),
    # URL pattern for the AgentProfileReadonlyView
    url(
        regex=r'^~agent/profile_readonly$',
        view=views.AgentProfileReadonlyView.as_view(),
        name='~agent_profile_readonly'
    ),
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
        regex=r'^~agent_pro_card/$',
        view=views.AgentProCardView.as_view(),
        name='~agent_pro_card'
    ),
    # URL pattern for the AgentCertificationsCreateView
    url(
        regex=r'^~agent_pro_card_qualification/$',
        view=views.AgentQualificationCreateView.as_view(),
        name='~agent_pro_card_qualification'
    ),
    # URL pattern for the AgentCertificationsCreateView
    url(
        regex=r'^~agent_various/$',
        view=views.AgentVariousView.as_view(),
        name='~agent_various'
    ),
    url(
        regex=r'^~agent_pdf/$',
        view=HelloPDFView.as_view(),
        name='~agent_pdf'
    ),
)
