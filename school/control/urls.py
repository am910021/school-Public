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
from .views import CAdminLogin, CMain, CMenu, CMenuAdd, CMenuDelete, CItem, CItemAdd, CItemDelete
from .views import CApps, CAppAdd, CAppDelete, CMenuEdit, CMenuMove, CResetOrder, CItemEdit
from .views import CItemMove, CAppEdit, CAppDownload

urlpatterns = [
    url(r'^main/$', CMain.as_view(), name='main'),
    url(r'^order/reset/$', CResetOrder.as_view(), name='orderReset'),
    
    url(r'^menu/$', CMenu.as_view(), name='menu'),
    url(r'^menu/add/$', CMenuAdd.as_view(), name='menuAdd'),
    url(r'^menu/del/$', CMenuDelete.as_view(), name='menuDel'),
    url(r'^menu/edit/(?P<menuID>[\w\-]+)/$', CMenuEdit.as_view(), name='menuEdit'),
    url(r'^menu/move/$', CMenuMove.as_view(), name='menuMove'),
    #url(r'^menu/view/(?P<menuID>[\w\-]+)/$', views.category, name='category'),
    
    url(r'^item/$', CItem.as_view(), name='item'),
    url(r'^item/add/$', CItemAdd.as_view(), name='itemAdd'),
    url(r'^item/add/(?P<menuID>[\w\-]+)/$', CItemAdd.as_view(), name='itemAddBy'),
    url(r'^item/del/$', CItemDelete.as_view(), name='itemDel'),
    url(r'^item/edit/(?P<itemID>[\w\-]+)/$', CItemEdit.as_view(), name='itemEdit'),
    url(r'^item/move/$', CItemMove.as_view(), name='itemMove'),
    url(r'^item/(?P<menuID>[\w\-]+)/$', CItem.as_view(), name='itemBy'),

    
    url(r'^apps/del/$', CAppDelete.as_view(), name='appDel'),
    url(r'^apps/(?P<itemID>[\w\-]+)/$', CApps.as_view(), name='apps'),
    url(r'^apps/add/(?P<itemID>[\w\-]+)/$', CAppAdd.as_view(), name='appAdd'),
    url(r'^apps/download/(?P<appID>[\w\-]+)/$', CAppDownload.as_view(), name='appDownload'),
    #url(r'^apps/edit/(?P<appID>[\w\-]+)/$', CAppEdit.as_view(), name='appEdit'),
    #url(r'^demo/(?P<demoID>[0-9]+)/$', ShowDemo.as_view(), name='demo'),
]
