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

'''
TODO:
* Error msg pages: 404, 405, 403, 400, 500

* user registration functionality corresponding to '/register' and POST method.
    form data: name(text), passwd(text)

* user login functionality corresponding to '/login' and POST method.
    form data: name(text), passwd(text)

* user login page corresponding to '/login' and GET method.

* user attach account functionality corresponding to '/attach/facebook' and
'/attach/twitter' with POST method.
    form data: name(text), passwd(text)
'''
urlpatterns = [
    url(r'^register$', views.register),
    url(r'^login$', views.log_in),
    url(r'^logout$', views.log_out),
    url(r'^attach/(?P<app_name>[a-z]+)', views.attach),
    url(r'^show/twitter$', views.show_twitters)
]
