# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views
from agent.views import ModalView


urlpatterns = patterns('',
    # URL pattern for the AgentHomeView
    url(
        regex=r'^landing$',
        view=views.ClientLandingView.as_view(),
        name='landing'
    ),
    url(
        regex=r'^~client/home$',
        view=views.ClientHomeView.as_view(),
        name='~client_home'
    ),
    url(
        regex=r'^home$',
        view=views.ClientHomeView.as_view(),
        name='client_home'
    ),
    url(
        regex=r'^~client/selection/add$',
        view=views.SelectionAddView.as_view(),
        name='~add_selection'
    ),
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
        regex=r'^~client/selection/list/$',
        view=views.selection_list_view,
        name='~selection_list_view',
    ),
    url(
        regex=r'^~client/selection/list_json/$',
        view=views.SelectionListJsonView.as_view(),
        name='~selection_list_json'
    ),
    url(
        regex=r'^filter/(?P<selectionid>\d+)/$',
        view=views.agent_filter_view,
        name='~agent_filter_view',
    ),
    url(
        regex=r'^list_json/$',
        view=views.AgentListJsonView.as_view(),
        name='~agent_list_json',
    ),
    url(
        regex=r'^~selection/delete/(?P<selectionid>\d+)/$',
        view=views.SelectionDeleteView.as_view(),
        name='~selection_delete_view',
    ),
    url(r'^add_agent_to_selection/$', views.add_agent_to_selection, name='add_agent'),
    url(r'^remove_agent_from_selection/$', views.remove_agent_from_selection, name='remove_agent'),
)
