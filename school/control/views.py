import os, zipfile, shutil
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from main.views import BaseView
from main.models import Menu, Item, ShinyApp, Setting
from .forms  import FMenu, FItem, FShinyApp
# Create your views here.

def admin_required(fun):
    def auth(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(settings.LOGIN_URL +'?next=%s' % request.path)
        if not request.user.is_superuser==True:
            return redirect(reverse('main:main'))
        return fun(request, *args, **kwargs)
    return auth

class AdminRequiredMixin(object):
    @classmethod
    def as_view(self):
        return admin_required(super(AdminRequiredMixin, self).as_view())


def manager_required(fun):
    def auth(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(settings.LOGIN_URL +'?next=%s' % request.path)
        if request.user.detail.type<1:
            return redirect(reverse('main:main'))
        return fun(request, *args, **kwargs)
    return auth

class ManagerRequiredMixin(object):
    @classmethod
    def as_view(self):
        return manager_required(super(ManagerRequiredMixin, self).as_view())


class ManagerBase(ManagerRequiredMixin, BaseView):
    #base_template_name = 'developer/base.html'
    template_dir_name = "control/"
    
    def __init__(self, *args, **kwargs):
        super(ManagerBase, self).__init__(*args, **kwargs)
        self.page_title="管理者-"+self.page_title
        self.template_name = self.template_dir_name+self.template_name


class AdminBase(AdminRequiredMixin, BaseView):
    #base_template_name = 'developer/base.html'
    template_dir_name = "control/"
    
    def __init__(self, *args, **kwargs):
        super(AdminBase, self).__init__(*args, **kwargs)
        self.page_title="管理者"+self.page_title
        self.template_name = self.template_dir_name+self.template_name
        
        
class CAdminLogin(AdminBase):
    def get(self, request, *args, **kwargs):
        return redirect('/control/admin/')
        
class CMain(ManagerBase):
    template_name = 'main.html' # xxxx/xxx.html
    page_title = '首頁' # title

    def get(self, request, *args, **kwargs):
        return super(CMain, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super(CMain, self).post(request, *args, **kwargs)
    
class CMenu(ManagerBase):
    template_name = 'menu/menu.html' # xxxx/xxx.html
    page_title = '選單管理' # title

    def get(self, request, *args, **kwargs):
        kwargs['menulist'] = Menu.objects.all()
        return super(CMenu, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super(CMenu, self).post(request, *args, **kwargs)
    
class CMenuView(ManagerBase):
    template_name = 'menu/menu.html' # xxxx/xxx.html
    page_title = '選單管理' # title

    def get(self, request, *args, **kwargs):
        kwargs['menulist'] = Menu.objects.all()
        return super(CMenu, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super(CMenu, self).post(request, *args, **kwargs)
        
class CMenuAdd(ManagerBase):
    template_name = 'menu/add.html' # xxxx/xxx.html
    page_title = '選單增加' # title
    
    def get(self, request, *args, **kwargs):
        kwargs['form'] = FMenu()
        return super(CMenuAdd, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = FMenu(request.POST)
        if not form.is_valid():
            kwargs['form'] = form
            return super(CMenuAdd, self).post(request, *args, **kwargs)
        
        form.save()
        messages.success(request, request.POST.get('name')+'選單新增成功。')
        return redirect(reverse('control:menu'))
    
    
class CMenuDelete(ManagerBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title
    def get(self, request, *args, **kwargs):
        return redirect(reverse('control:main'))
    
    def post(self, request, *args, **kwargs):
        if 'menuID' not in request.POST:
            messages.success(request, request.POST.get('menuName')+'選單刪除失敗。')
        try:
            menu = Menu.objects.get(id=request.POST.get('menuID'))
            menu.delete()
            messages.success(request, request.POST.get('menuName')+'選單刪除成功。')
        except Exception as e:
            print(e)
            messages.success(request, request.POST.get('menuName')+'選單刪除失敗。')
        return redirect(reverse('control:menu'))
    
    
class CItem(ManagerBase):
    template_name = 'item/item.html' # xxxx/xxx.html
    page_title = '項目管理' # title

    def get(self, request, *args, **kwargs):
        menuID = kwargs['menuID'] if 'menuID' in kwargs else None
        if not menuID:
            kwargs['itemlist'] = Item.objects.all()
        else: 
            menu = Menu.objects.get(id=menuID)
            kwargs['menuName'] = menu.name
            kwargs['itemlist'] = Item.objects.filter(menu=menu)    

        return super(CItem, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super(CItem, self).post(request, *args, **kwargs)
    
class CItemAdd(ManagerBase):
    template_name = 'item/add.html' # xxxx/xxx.html
    page_title = '新增項目' # title

    def get(self, request, *args, **kwargs):
        menuID = kwargs['menuID'] if 'menuID' in kwargs else None
        print(menuID)
        if not menuID:
            kwargs['form'] = FItem()
        else:
            kwargs['form'] = FItem(menu=menuID)
        return super(CItemAdd, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = FItem(request.POST)
        if not form.is_valid():
            kwargs['form'] = form
            return super(CItemAdd, self).post(request, *args, **kwargs)
        try:
            menu = form.save(commit=False)
            menu.menu=Menu.objects.get(id=request.POST.get('menu'))
            menu.save()
            messages.success(request, request.POST.get('name')+'指標加入功成。')
        except Exception as e:
            messages.success(request, request.POST.get('name')+'指標加入失敗。')
            print(e)
        return redirect(reverse('control:item'))
    
class CItemDelete(ManagerBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title
    
    def get(self, request, *args, **kwargs):
        return redirect(reverse('control:item'))
    
    def post(self, request, *args, **kwargs):
        if 'itemID' not in request.POST:
            messages.success(request, request.POST.get('itemName')+'指標刪除失敗。')
        try:
            item = Item.objects.get(id=request.POST.get('itemID'))
            item.delete()
            messages.success(request, request.POST.get('itemName')+'指標刪除成功。')
        except Exception as e:
            print(e)
            messages.success(request, request.POST.get('itemName')+'指標刪除失敗。')
        return redirect(reverse('control:item'))
    
    
class CApps(ManagerBase):
    template_name = 'apps/apps.html' # xxxx/xxx.html
    page_title = 'apps/apps.html' # title

    def get(self, request, *args, **kwargs):
        itemID = kwargs['itemID'] if 'itemID' in kwargs else None
        item=Item.objects.get(id=itemID)
        kwargs['itemName'] = item.name
        kwargs['apps'] = ShinyApp.objects.filter(item=item)
        return super(CApps, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super(CApps, self).post(request, *args, **kwargs)
    
class CAppAdd(ManagerBase):
    template_name = 'apps/add.html' # xxxx/xxx.html
    page_title = '上傳APP' # title

    def get(self, request, *args, **kwargs):
        item = kwargs['itemID'] if 'itemID' in kwargs else None
        if not item:
            return redirect(reverse('control:item'))
        
        kwargs['form'] = FShinyApp(item=item)
        return super(CAppAdd, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = FShinyApp(request.POST)
        if not form.is_valid():
            kwargs['form'] = form
            return super(CAppAdd, self).post(request, *args, **kwargs)
        
        if 'upload_file' not in request.FILES:
            kwargs['not_found']="*請選擇檔案"
            kwargs['form'] = form
            return super(CAppAdd, self).post(request, *args, **kwargs)
        
        try:
            config = Setting.objects.get(name="dirPath")
            dirName = str(request.POST.get('dirName')).replace(" ","-")
            if os.path.exists(config.c1+dirName):
                kwargs['dir_exists'] = "* 資料夾已存在"
                kwargs['form'] = form
                return super(CAppAdd, self).post(request, *args, **kwargs)
            
            file = request.FILES['upload_file']
            os.makedirs(config.c1+dirName)
            zip_ref = zipfile.ZipFile(file, 'r')
            zip_ref.extractall(config.c1+dirName)
            zip_ref.close()
        except Exception as e:
            print(e)
            kwargs['file_error'] = "*檔案格式錯誤"
            kwargs['form'] = form
            return super(CAppAdd, self).post(request, *args, **kwargs)
        form = form.save(commit=False)
        form.user = request.user
        form.dirName = dirName
        form.save()
        messages.success(request, 'APP上傳成功。')
        return redirect(reverse('control:apps', args=(request.POST.get('item'),)))
    
    
class CAppDelete(ManagerBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title
    def post(self, request, *args, **kwargs):
        print("post")
        try:
            appID = request.POST.get('appID')
            shiny = ShinyApp.objects.get(id=appID)
            itemID = shiny.item.id
            shinyName = shiny.name
            
            config = Setting.objects.get(name="dirPath")
            if os.path.exists(config.c1+shiny.dirName):
                shutil.rmtree(config.c1+shiny.dirName)
                shiny.delete()
            messages.success(request, shinyName+'刪除成功。')
        except Exception as e:
            messages.success(request, shinyName+'刪除失敗。')
            print(e)
         
        print("post end") 
        return redirect(reverse('control:apps', args=(itemID,)))
    
    
    
    
        