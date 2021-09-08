from django.contrib import admin
from django.urls import path
from django.conf.urls import  include, url
from django.conf import settings
from django.template import RequestContext
from django import template
from django.template import Context
from rest_framework.schemas import get_schema_view
from MySolarSentinelAdmin import views

urlpatterns = [
    url("^$", views.dashboard, name="dashboard"),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url("^customer/(?P<customer_id>\d+)/$", views.view_customer, name="view_customer"),
    url("^supportTicket/(?P<customer_id>\d+)/$", views.view_supportTicket, name="supportTicket"),
    url("^create_ticket/(?P<customer_id>\d+)/$", views.create_ticket, name="create_ticket"),
    url("^edit_ticket/(?P<customer_id>\d+)/$", views.edit_ticket, name="edit_ticket"),
    url("^close_ticket/(?P<customer_id>\d+)/$", views.close_ticket, name="close_ticket"),
    url(r'^support_tickets/$', views.support_tickets, name='support_tickets'),
]
