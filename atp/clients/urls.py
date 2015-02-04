# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views
from agent.views import ModalView


urlpatterns = patterns('',
    # URL pattern for the AgentHomeView
    url(
        regex=r'^~client/home$',
        view=views.ClientHomeView.as_view(),
        name='~client_home'
    ),
    url(
        regex=r'^~client/selection/add$',
        view=views.SelectionView.as_view(),
        name='~add_selection'
    ),
    #url(
        #regex=r'^~client/selection/agent/detail/modal/(?P<pk>\d+)/$',
        #view=AgentDetailModal.as_view(),
        #name='~agent_detail_modal'
    #),
    url(
        regex=r'^~client/selection/agent/detail/modal/(?P<pk>\d+)/$',
        view=ModalView.as_view(),
        name='~agent_detail_modal'
    ),
    url(
        regex=r'^~client/detail/modal/(?P<pk>\d+)/$',
        view=ModalView.as_view(),
        name='~modal_view'
    ),
    url(
        regex=r'^~client/selection/list$',
        view=views.SelectionListView.as_view(),
        name='~list_selection'
    ),
    url(
        regex=r'^filter/(?P<selectionid>\d+)/$',
        view=views.filter_view,
        name='agent_filter',
    ),
    url(
        regex=r'^list_json/$',
        view=views.AgentListJson.as_view(),
        name='agent_list_json',
    ),
    url(r'^add_agent_to_selection/$', views.add_agent_to_selection, name='add_agent'),
    #url(r'^~client/data/agents_list/$', views.agents_list, name='agents_list'),
    url(r'^remove_agent_from_selection/$', views.remove_agent_from_selection, name='remove_agent'),
)
