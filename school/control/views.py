import os, zipfile, shutil
from io import StringIO
from django.http import HttpResponseNotFound, HttpResponse
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
    page_title = ""
    template_name = ""
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
        menu = Menu.objects.all()
        kwargs['menulist'] = menu.order_by('order')
        return super(CMenu, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super(CMenu, self).post(request, *args, **kwargs)
    
class CMenuView(ManagerBase):
    template_name = 'menu/menu.html' # xxxx/xxx.html
    page_title = '選單管理' # title

    def get(self, request, *args, **kwargs):
        kwargs['menulist'] = Menu.objects.all().order_by('order')
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
        
        menu = form.save()
        menu.order = menu.id
        menu.save()
        messages.success(request, request.POST.get('name')+'選單新增成功。')
        return redirect(reverse('control:menu'))
    
class CMenuEdit(ManagerBase):
    template_name = 'menu/edit.html'
    page_title = '' # title
    
    def get(self, request, *args, **kwargs):
        try:
            menu = Menu.objects.get(id=kwargs['menuID'])
            kwargs['menuName'] = menu.name
            kwargs['menuID'] = menu.id
        except:
            return redirect(reverse('control:menu'))
        if menu:
            kwargs['form'] = FMenu(instance=menu)
            self.page_title = menu.name+"-編輯"
        return super(CMenuEdit, self).post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            menu = Menu.objects.get(id=request.POST.get('menuID'))
            name = menu.name
        except:
            return redirect(reverse('control:menu'))
            
        form = FMenu(request.POST, instance=menu)
        if not form.is_valid():
            kwargs['form'] = form
            kwargs['menuName'] = menu.name
            kwargs['menuID'] = menu.id
            return super(CMenuEdit, self).post(request, *args, **kwargs)
            
        saved = form.save()
        messages.success(request, saved.name+'('+name+')'+' 修改成功。')
        return redirect(reverse('control:menu'))

class CMenuMove(ManagerBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title
    def post(self, request, *args, **kwargs):
        up = int(request.POST.get('UP')) if request.POST.get('UP')!="" else None
        down = int(request.POST.get('DOWN')) if request.POST.get('DOWN')!="" else None
        menu = Menu.objects.all().order_by("order")
        menuLen = len(list(menu))
        temp = menu[0]
        temp2 = menu[menuLen-1]
        if temp.id == up:
            messages.success(request, temp.name+'已經在最上方。')
            return redirect(reverse('control:menu'))
        elif temp2.id==down:
            messages.success(request, temp2.name+'已經在最下方。')
            return redirect(reverse('control:menu'))
        if up:
            for i in range(1,menuLen):
                if menu[i].id==up:
                    tmp = menu[i].order
                    menu[i].order=menu[i-1].order
                    menu[i-1].order=menu[i].order
                    menu[i-1].order=tmp
                    menu[i].save()
                    menu[i-1].save()
                    messages.success(request, menu[i].name+'成功往上移動。')
                    break
        elif down:
            for i in range(0,menuLen-1):
                if menu[i].id==down:
                    tmp = menu[i].order
                    menu[i].order=menu[i+1].order
                    menu[i+1].order=menu[i].order
                    menu[i+1].order=tmp
                    menu[i].save()
                    menu[i+1].save()
                    messages.success(request, menu[i].name+'成功往下移動。')
                    break
        return redirect(reverse('control:menu'))
    
class CResetOrder(ManagerBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title
    def post(self, request, *args, **kwargs):
        do = request.POST.get('resetName') if request.POST.get('resetName')!="" else None
        if do=="menu":
            menu = Menu.objects.all().order_by("id")
            for i in menu:
                i.order = i.id
                i.save()
            messages.success(request, '重置排序成功。')
            return redirect(reverse('control:menu'))
        elif do=="item":
            where = request.POST.get('where') if request.POST.get('where')!="-1" else None
            if where:
                menu=Menu.objects.get(id=where)
                item = Item.objects.filter(menu=menu).order_by("id")
                for i in item:
                    i.order = i.id
                    i.save()
                messages.success(request, '重置排序成功。')
                return redirect(reverse('control:itemBy', args=(menu.id,)))
            else:
                item = Item.objects.all().order_by("id")
                for i in item:
                    i.order = i.id
                    i.save()
                messages.success(request, '重置排序成功。')
                return redirect(reverse('control:item'))

    
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
            kwargs['itemlist'] = Item.objects.all().order_by('order')
            kwargs['menuID'] = -1
        else: 
            menu = Menu.objects.get(id=menuID)
            kwargs['menuName'] = menu.name
            kwargs['menuID'] = menu.id
            kwargs['itemlist'] = Item.objects.filter(menu=menu).order_by('order')   

        return super(CItem, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super(CItem, self).post(request, *args, **kwargs)
    
class CItemEdit(ManagerBase):
    template_name = 'item/edit.html' # xxxx/xxx.html
    page_title = '' # title

    def get(self, request, *args, **kwargs):
        try:
            item = Item.objects.get(id=kwargs['itemID'])
            kwargs['itemName'] = item.name
            kwargs['itemID'] = item.id
        except:
            return redirect(reverse('control:item'))
        if item:
            kwargs['form'] = FItem(instance=item,menu=item.menu.id)
            kwargs['menuID'] = item.menu.id
            self.page_title = item.name+"-編輯"
        return super(CItemEdit, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            item = Item.objects.get(id=request.POST.get('itemID'))
            name = item.name
        except:
            return redirect(reverse('control:item'))
            
        form = FItem(request.POST, instance=item)
        if not form.is_valid():
            kwargs['form'] = form
            kwargs['itemName'] = item.name
            kwargs['itemID'] = item.id
            kwargs['menuID'] = item.menu.id
            return super(CItemEdit, self).post(request, *args, **kwargs)
            
        saved = form.save()
        messages.success(request, saved.name+'('+name+')'+' 修改成功。')
        return redirect(reverse('control:itemBy', args=(item.menu.id,)))
    
    
class CItemMove(ManagerBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title
    
    def post(self, request, *args, **kwargs):
        up = int(request.POST.get('UP')) if request.POST.get('UP')!="" else None
        down = int(request.POST.get('DOWN')) if request.POST.get('DOWN')!="" else None
        
        if up:
            tempItem = Item.objects.get(id=up)
            item = Item.objects.filter(menu=tempItem.menu).order_by("order")
            menuID=tempItem.menu.id
        elif down:
            tempItem = Item.objects.get(id=down)
            item = Item.objects.filter(menu=tempItem.menu).order_by("order")
            menuID=tempItem.menu.id
        itemLen = len(list(item))
        temp = item[0]
        temp2 = item[itemLen-1]

        
        if temp.id == up:
            messages.success(request, temp.name+'已經在最上方。')
            return redirect(reverse('control:itemBy', args=(menuID,)))
        elif temp2.id==down:
            messages.success(request, temp2.name+'已經在最下方。')
            return redirect(reverse('control:itemBy', args=(menuID,)))
        
        if up:
            for i in range(1,itemLen):
                if item[i].id==up:
                    tmp = item[i].order
                    item[i].order=item[i-1].order
                    item[i-1].order=item[i].order
                    item[i-1].order=tmp
                    item[i].save()
                    item[i-1].save()
                    messages.success(request, item[i].name+'成功往上移動。')
                    break
        elif down:
            for i in range(0,itemLen-1):
                if item[i].id==down:
                    tmp = item[i].order
                    item[i].order=item[i+1].order
                    item[i+1].order=item[i].order
                    item[i+1].order=tmp
                    item[i].save()
                    item[i+1].save()
                    messages.success(request, item[i].name+'成功往下移動。')
                    break
        return redirect(reverse('control:itemBy', args=(menuID,)))
    
    
class CItemAdd(ManagerBase):
    template_name = 'item/add.html' # xxxx/xxx.html
    page_title = '新增項目' # title

    def get(self, request, *args, **kwargs):
        menuID = kwargs['menuID'] if 'menuID' in kwargs else None
        if not menuID:
            kwargs['form'] = FItem()
        else:
            kwargs['form'] = FItem(menu=menuID)
            
        return super(CItemAdd, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = FItem(request.POST)
        id = 0
        if not form.is_valid():
            kwargs['form'] = form
            return super(CItemAdd, self).post(request, *args, **kwargs)
        try:
            menu = form.save(commit=False)
            id = request.POST.get('menu')
            menu.menu=Menu.objects.get(id=id)
            menu.save()
            menu.order = menu.id
            menu.save()
            messages.success(request, request.POST.get('name')+'指標加入功成。')
        except Exception as e:
            messages.success(request, request.POST.get('name')+'指標加入失敗。')
            print(e)
        return redirect(reverse('control:itemBy', args=(id,)))
    
    
    
    
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
            menu = item.menu
            item.delete()
            messages.success(request, request.POST.get('itemName')+'指標刪除成功。')
            return redirect(reverse('control:itemBy', args=(menu.id,)))
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
        kwargs['menuID'] = item.menu.id
        kwargs['apps'] = ShinyApp.objects.filter(item=item).order_by('order')
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
            
            os.makedirs(config.c1+dirName+"/zip/")
            fd = open(config.c1+dirName+'/zip/'+file.name, 'wb')
            for chunk in file.chunks():
                fd.write(chunk)
            fd.close()

            
            form = form.save(commit=False)
            form.user = request.user
            form.dirName = dirName
            form.fileName = file.name
            form.fileType = file.content_type
            form.save()
            form.order = form.id
            form.save()
            messages.success(request, 'APP上傳成功。')
        except Exception as e:
            print(e)
            kwargs['file_error'] = "*檔案格式錯誤"
            kwargs['form'] = form
            messages.success(request, 'APP上傳失敗。')
            return super(CAppAdd, self).post(request, *args, **kwargs)
        return redirect(reverse('control:apps', args=(request.POST.get('item'),)))
    
class CAppDownload(ManagerBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title

    def get(self, request, *args, **kwargs):
        try:
            app = ShinyApp.objects.get(id=kwargs['appID'])
            config = Setting.objects.get(name="dirPath")
        except:
            return HttpResponseNotFound('<h1>檔案不存在</h1>') 
 
        response = HttpResponse(open(config.c1+app.dirName+"/zip/"+app.fileName, 'rb').read(),content_type=app.fileType)
        response['Content-Disposition'] = 'attachment; filename=%s' % app.fileName

        return response

    
class CAppEdit(ManagerBase):
    template_name = 'apps/edit.html' # xxxx/xxx.html
    page_title = '' # title

    def get(self, request, *args, **kwargs):
        try:
            app = ShinyApp.objects.get(id=kwargs['appID'])
            kwargs['appName'] = app.name
            kwargs['appID'] = app.id
        except:
            return redirect(reverse('control:item'))
        if app:
            kwargs['form'] = FShinyApp(instance=app, item=app.item.id)
            self.page_title = app.name+"-編輯"
        return super(CAppEdit, self).post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            app = ShinyApp.objects.get(id=request.POST.get('appID'))
            form = FShinyApp(request.POST, instance=app)
        except:
            return redirect(reverse('control:item'))
        
            kwargs['appName'] = app.name
            kwargs['appID'] = app.id
        if not form.is_valid():
            kwargs['form'] = form
            return super(CAppEdit, self).post(request, *args, **kwargs)   
        
        if 'upload_file' not in request.FILES:
            kwargs['not_found']="*請選擇檔案"
            kwargs['form'] = form
            return super(CAppEdit, self).post(request, *args, **kwargs)
        
        try:
            config = Setting.objects.get(name="dirPath")
            dirName = str(request.POST.get('dirName')).replace(" ","-")

            if os.path.exists(config.c1+app.dirName):
                shutil.rmtree(config.c1+app.dirName)
            
            file = request.FILES['upload_file']
            os.makedirs(config.c1+dirName)
            zip_ref = zipfile.ZipFile(file, 'r')
            zip_ref.extractall(config.c1+dirName)
            zip_ref.close()
            
            form = form.save(commit=False)
            form.user = request.user
            form.dirName = dirName
            form.save()
            form.order = form.id
            form.save()
        except:
            kwargs['file_error'] = "*檔案格式錯誤"
            kwargs['form'] = form
            messages.success(request, 'APP更新失敗。')
            return super(CAppAdd, self).post(request, *args, **kwargs)
        
        messages.success(request, 'APP更新成功。')
        return redirect(reverse('control:apps', args=(request.POST.get('item'),)))
    
    
class CAppDelete(ManagerBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title
    def post(self, request, *args, **kwargs):
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
    
    
    
    
        