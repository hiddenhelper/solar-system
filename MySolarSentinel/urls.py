"""MySolarSentinel URL Configuration
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from MySolarSentinelAdmin import views as admin_view
from MySolarSentinelAPI import views as SolarAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('MySolarSentinelAPI.urls')),
    path('page/admin/', include('MySolarSentinelAdmin.urls')),
    url(r'^accounts/login/$', admin_view.login, name='login'),
    url(r'^accounts/logout/$', admin_view.logout, name='logout'),

]
