"""school URL Configuration

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
from .views import Main, Uplist, Upload, Remove, Config, ConfigShiny, ConfigSchoolAPI, ConfigShinyHost, CongigKey, ShowDemo

urlpatterns = [
    url(r'^$', Main.as_view(), name='main'),
    url(r'^list/$', Uplist.as_view(), name='list'),
    url(r'^upload/$', Upload.as_view(), name='upload'),
    url(r'^remove/$', Remove.as_view(), name='remove'),
    
    url(r'^demo/(?P<demoID>[0-9]+)/$', ShowDemo.as_view(), name='demo'),
]
