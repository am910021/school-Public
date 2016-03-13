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
from .views import schoolAPI,schoolAPI2, templateJSON, CSVapi,CSVapi2

urlpatterns = [
    url(r'^templatejson/(?P<year>[0-9]+)/(?P<semester>[0-2]?)/$', templateJSON),
    
    url(r'^school/(?P<year>[0-9]+)/(?P<semester>[0-2]?)/$', schoolAPI),
    #url(r'^school/(?P<startYear>[0-9]+)-(?P<endYear>[0-9]+)/(?P<semester>[0-2]?)/$', schoolAPI2),
    
    #url(r'^query/(?P<year>[0-9]+)/(?P<semester>[0-2]?)/$', CSVapi),
    #url(r'^query/(?P<year>[0-9]+)/(?P<semester>[0-2]?)/(?P<category>.+)/$', CSVapi2),
    #url(r'^query/(?P<startYear>[0-9]+)-(?P<endYear>[0-9]+)/(?P<semester>[0-2]?)/$', CSVapi2),
    #url(r'^query/(?P<startYear>[0-9]+)-(?P<endYear>[0-9]+)/(?P<semester>[0-2]?)/(?P<category>\w+)/$', CSVapi2),
]
