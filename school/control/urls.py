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
from .views import CAdminLogin, CMain, CResetOrder, CMove
from .views import CMenu, CMenuAdd, CMenuDelete, CMenuEdit
from .views import CItem, CItemAdd, CItemDelete, CItemEdit
from .views import CApps, CAppAdd, CAppDelete, CAppEdit, CAppDownload
from .views import CConfig, CConfigSchoolAPI, CConfigShiny, CCongigKey
from .views import CPermissions, CPermissionsAdd, CPermissionsDetail, CPermissionsEdit, CPermissionsRemove
from .views import CAccount, CAccountAdd, CAccountEdit, CAccountRemove, CAccountDetail, CAccountAdd3nd


urlpatterns = [
    url(r'^main/$', CMain.as_view(), name='main'),
    url(r'^order/reset/$', CResetOrder.as_view(), name='orderReset'),
    url(r'^move/$', CMove.as_view(), name='move'),
    
    url(r'^menu/$', CMenu.as_view(), name='menu'),
    url(r'^menu/add/$', CMenuAdd.as_view(), name='menuAdd'),
    url(r'^menu/del/$', CMenuDelete.as_view(), name='menuDel'),
    url(r'^menu/edit/(?P<menuID>[0-9]+)/$', CMenuEdit.as_view(), name='menuEdit'),
    #url(r'^menu/view/(?P<menuID>[0-9]+)/$', views.category, name='category'),
    
    url(r'^item/$', CItem.as_view(), name='item'),
    url(r'^item/add/$', CItemAdd.as_view(), name='itemAdd'),
    url(r'^item/add/(?P<menuID>[0-9]+)/$', CItemAdd.as_view(), name='itemAddBy'),
    url(r'^item/del/$', CItemDelete.as_view(), name='itemDel'),
    url(r'^item/edit/(?P<itemID>[0-9]+)/$', CItemEdit.as_view(), name='itemEdit'),
    url(r'^item/(?P<menuID>[0-9]+)/$', CItem.as_view(), name='itemBy'),

    
    url(r'^apps/del/$', CAppDelete.as_view(), name='appDel'),
    url(r'^apps/add/(?P<itemID>[0-9]+)/$', CAppAdd.as_view(), name='appAdd'),
    url(r'^apps/edit/(?P<appID>[0-9]+)/$', CAppEdit.as_view(), name='appEdit'),
    url(r'^apps/download/(?P<appID>[0-9]+)/$', CAppDownload.as_view(), name='appDownload'),
    url(r'^apps/(?P<itemID>[0-9]+)/$', CApps.as_view(), name='apps'),
    
    url(r'config/$', CConfig.as_view(), name="config"),
    url(r'config/api/$', CConfigSchoolAPI.as_view(), name="configAPI"),
    url(r'config/app/$', CConfigShiny.as_view(), name="configAPP"),
    url(r'config/key/$', CCongigKey.as_view(), name="configKEY"),
    #url(r'^demo/(?P<demoID>[0-9]+)/$', ShowDemo.as_view(), name='demo'),
    
    url(r'permissions/$', CPermissions.as_view(), name="permissions"),
    url(r'permissions/add/$', CPermissionsAdd.as_view(), name="permissionsAdd"),
    url(r'permissions/edit/(?P<id>[0-9]+)/$', CPermissionsEdit.as_view(), name="permissionsEdit"),
    url(r'permissions/detail/(?P<id>[0-9]+)/$', CPermissionsDetail.as_view(), name="permissionsDetail"),
    url(r'permissions/remove/$', CPermissionsRemove.as_view(), name="permissionsRemove"),
    
    url(r'account/$', CAccount.as_view(), name="account"),
    url(r'account/add/$', CAccountAdd.as_view(), name="accountAdd"),
    url(r'account/add/3nd/$', CAccountAdd3nd.as_view(), name="accountAdd3nd"),
    url(r'account/edit/(?P<id>[0-9]+)/$', CAccountEdit.as_view(), name="accountEdit"),
    url(r'account/detail/(?P<id>[0-9]+)/$', CAccountDetail.as_view(), name="accountDetail"),
    url(r'account/remove/$', CAccountRemove.as_view(), name="accountRemove"),
]
