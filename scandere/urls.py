from nmaper import views
from nmaper.admin import views as adm_views
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as views_django
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^console/clear_logs/?$', adm_views.clear_logs, name='clear-logs'),
    url(r'^console/', admin.site.urls),
    url(r'^login/$', views_django.login, name='login')   
]