# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views
from agent.views import AgentDetailModal


urlpatterns = patterns('',
    # URL pattern for the AgentHomeView
    url(
        regex=r'^~client/home$',
        view=views.ClientHomeView.as_view(),
        name='~client_home'
    ),
    url(
        #regex=r'^~client/data$',
        regex=r'^~client/data(?P<selectionid>\w{0,50})$',
        view=views.DataTableView.as_view(),
        name='~client_datatable'
    ),
    url(
        regex=r'^~client/selection/add$',
        view=views.SelectionView.as_view(),
        name='~add_selection'
    ),
    url(
        regex=r'^~client/selection/agent/detail/modal/(?P<pk>\d+)/$',
        view=AgentDetailModal.as_view(),
        name='~agent_detail_modal'
    ),
    url(
        regex=r'^~client/selection/list$',
        view=views.SelectionListView.as_view(),
        name='~list_selection'
    ),
    url(r'^add_agent_to_selection/$', views.add_agent_to_selection, name='add_agent'),
    url(r'^remove_agent_from_selection/$', views.remove_agent_from_selection, name='remove_agent'),
)
