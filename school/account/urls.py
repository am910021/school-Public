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
import account.views as views
from .views import CCenter, CModify, CModifyPwd, CPermissions, CAccountAuth

urlpatterns = [
    #url(r'^auth/(?P<token>\w+)/$', CAccountAuth.as_view(), name="accountAuth"),    
    url(r'^auth/(?P<token>[A-Fa-f0-9]+)/$', CAccountAuth.as_view(), name="accountAuth"),      
    url(r'^login/$', views.Login.as_view(), name='login'), 
    url(r'^signup/$', views.SignUp.as_view(), name='signup'), 
    url(r'^logout/$', views.Logout, name='logout'),
    
    url(r'^center/$', CCenter.as_view(), name='center'),  
    url(r'^modify/$', CModify.as_view(), name='modify'),  
    url(r'^modify/pwd/$', CModifyPwd.as_view(), name='modifyPWD'),  
    url(r'^permissions/$', CPermissions.as_view(), name='permissions'), 
    
]
