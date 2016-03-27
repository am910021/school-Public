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
from .views import schoolAPI,schoolAPI2, templateJSON, ArgsError, schoolAPI3, schoolAPI4

#studsem/104/1/, student, hstudent, class2/104/, sub, col, dep2, message, province, zip, entid, entsource, entqual, aborg, 


urlpatterns = [
    url(r'^templatejson/(?P<year>[0-9]+)/(?P<semester>[0-2]?)/$', templateJSON),
    
    #/case/103/10/10/
    url(r'^ir/case/(?P<startYear>[0-9]+)-(?P<endYear>[0-9]+)/(?P<key1>[0-9]+)/(?P<key2>[0-9]+)/(?P<license>.+)/$', schoolAPI4),
    url(r'^ir/case/(?P<year>[0-9]+)/(?P<key1>[0-9]+)/(?P<key2>[0-9]+)/(?P<license>.+)/$', schoolAPI3),
    
    
    url(r'^ir/(?P<name>\w+)/(?P<startYear>[0-9]+)-(?P<endYear>[0-9]+)/(?P<semester>[0-2]?)/(?P<license>.+)/$', schoolAPI2),
    url(r'^ir/(?P<name>\w+)/(?P<startYear>[0-9]+)-(?P<endYear>[0-9]+)/(?P<license>.+)/$', schoolAPI2),
    
    url(r'^ir/(?P<name>\w+)/(?P<year>[0-9]+)/(?P<semester>[0-2]?)/(?P<license>.+)/$', schoolAPI),
    url(r'^ir/(?P<name>\w+)/(?P<year>[0-9]+)/(?P<license>.+)/$', schoolAPI),
    url(r'^ir/(?P<name>\w+)/(?P<license>.+)/$', schoolAPI),
    
    
    
    #url(r'^query/(?P<year>[0-9]+)/(?P<semester>[0-2]?)/$', CSVapi),
    #url(r'^query/(?P<year>[0-9]+)/(?P<semester>[0-2]?)/(?P<category>.+)/$', CSVapi2),
    #url(r'^query/(?P<startYear>[0-9]+)-(?P<endYear>[0-9]+)/(?P<semester>[0-2]?)/$', CSVapi2),
    #url(r'^query/(?P<startYear>[0-9]+)-(?P<endYear>[0-9]+)/(?P<semester>[0-2]?)/(?P<category>\w+)/$', CSVapi2),
    url(r'^.*', ArgsError),
]
