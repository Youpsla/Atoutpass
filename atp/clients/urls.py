# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    # URL pattern for the AgentHomeView
    url(
        regex=r'^~client/home$',
        view=views.ClientHomeView.as_view(),
        name='~client_home'
    ),
    url(
        regex=r'^~client/data$',
        view=views.DDataTableView.as_view(),
        name='~client_datatable'
    ),
    url(
        regex=r'^~client/selection$',
        view=views.SelectionView.as_view(),
        name='~selection'
    ),
)
