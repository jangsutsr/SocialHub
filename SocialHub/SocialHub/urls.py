"""SocialHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from main_app import views

urlpatterns = [
    url(r'^register$', views.register),
    url(r'^login$', views.log_in),
    url(r'^logout$', views.log_out),
    url(r'^attach/(?P<app_name>[a-z]+)$', views.attach),
    url(r'^show$', views.show),
    url(r'^history/(?P<offset>[0-9]+)$', views.history),
    url(r'^audio$', views.audio),
    url(r'^twitter$', views.twitter)
]
