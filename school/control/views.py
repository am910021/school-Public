import os, zipfile, shutil
from django.http import HttpResponseNotFound, HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from main.views import BaseView
from main.models import Menu, Item, ShinyApp, Setting, DBGroupName, DBGroupItem
from .models import ItemGroupManage, AccountManage
from .forms  import FMenu, FItem, FShinyApp, UserForm, UserProfileForm , UserEditForm
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
        if request.user.profile.type<1:
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
        #self.page_title="管理者"+self.page_title
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
        #messages.success(request, request.POST.get('name')+'選單新增成功。')
        messages.success(request,request.POST.get('name')+'選單新增成功。')
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
        #messages.success(request, saved.name+'('+name+')'+' 修改成功。')
        messages.success(request, saved.name+'('+name+')'+' 修改成功。')
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
            #messages.success(request, '重置排序成功。')
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
                #messages.success(request, '重置排序成功。')
                messages.success(request, '重置排序成功。')
                return redirect(reverse('control:itemBy', args=(menu.id,)))
            else:
                item = Item.objects.all().order_by("id")
                for i in item:
                    i.order = i.id
                    i.save()
                #messages.success(request, '重置排序成功。')
                messages.success(request, '重置排序成功。')
                return redirect(reverse('control:item'))

    
class CMenuDelete(ManagerBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title
    def get(self, request, *args, **kwargs):
        return redirect(reverse('control:main'))
    
    def post(self, request, *args, **kwargs):
        if 'menuID' not in request.POST:
            #messages.success(request, request.POST.get('menuName')+'選單刪除失敗。')
            messages.error(request, request.POST.get('menuName')+'選單刪除失敗。')
        try:
            menu = Menu.objects.get(id=request.POST.get('menuID'))
            menu.delete()
            #messages.success(request, request.POST.get('menuName')+'選單刪除成功。')
            messages.success(request, request.POST.get('menuName')+'選單刪除成功。')
        except Exception as e:
            print(e)
            #messages.success(request, request.POST.get('menuName')+'選單刪除失敗。')
            messages.error(request, request.POST.get('menuName')+'選單刪除失敗。')
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
            menu = item.menu
        except:
            return redirect(reverse('control:item'))
            
        form = FItem(request.POST, instance=item)
        if not form.is_valid():
            kwargs['form'] = form
            kwargs['itemName'] = item.name
            kwargs['itemID'] = item.id
            kwargs['menuID'] = item.menu.id
            return super(CItemEdit, self).post(request, *args, **kwargs)
        form = form.save()
        form.menu = Menu.objects.get(id=request.POST.get('menu'))
        form.save()
        
        item = Item.objects.filter(menu=menu)
        menu.itemQty = len(item)
        menu.activeQty = len(item.filter(isActive=True))
        menu.isActive = True if menu.activeQty > 0 else False
        menu.save()
        
        #messages.success(request, form.name+'('+name+')'+' 修改成功。')
        messages.success(request, form.name+'('+name+')'+' 修改成功。')
        return redirect(reverse('control:itemBy', args=(form.menu.id,)))
      
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
        if not form.is_valid():
            kwargs['form'] = form
            kwargs['menuID'] = request.POST.get('menu')
            return super(CItemAdd, self).post(request, *args, **kwargs)

        item = form.save(commit=False)
        item.menu=Menu.objects.get(id=request.POST.get('menu'))
        item.save()
        item.order = item.id
        item.save()
        #messages.success(request, request.POST.get('name')+'指標加入功成。')
        messages.success(request, request.POST.get('name')+'指標加入功成。')
        return redirect(reverse('control:itemBy', args=(item.menu.id,)))
    
    
class CItemDelete(ManagerBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title
    
    def get(self, request, *args, **kwargs):
        return redirect(reverse('control:item'))
    
    def post(self, request, *args, **kwargs): 
        try:
            item = Item.objects.get(id=request.POST.get('itemID'))
        except Exception as e:
            print(e)
            #messages.success(request,'指標刪除失敗。')
            messages.error(request, '指標刪除失敗。')
            return redirect(reverse('control:item'))
            
        item = Item.objects.get(id=request.POST.get('itemID'))
        menu = item.menu
        item.delete()
        #messages.success(request, request.POST.get('itemName')+'指標刪除成功。')
        messages.success(request, request.POST.get('itemName')+'指標刪除成功。')
        return redirect(reverse('control:itemBy', args=(menu.id,)))
    
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
        try:
            item = Item.objects.get(id=kwargs['itemID'])
        except:
            return redirect(reverse('control:item'))

        kwargs['menuID'] = item.menu.id
        kwargs['form'] = FShinyApp(item=item.id)
        return super(CAppAdd, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = FShinyApp(request.POST)
        kwargs['menuID'] = request.POST.get('menuID')
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
            messages.success(request, request.POST.get('name')+' APP上傳成功。')
        except Exception as e:
            print(e)
            kwargs['file_error'] = "*檔案格式錯誤"
            kwargs['form'] = form
            #messages.success(request, 'APP上傳失敗。')
            messages.error(request, request.POST.get('name')+' APP上傳失敗。')
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
            shiny = ShinyApp.objects.get(id=kwargs['appID'])
        except:
            return redirect(reverse('control:item'))
        
        kwargs['menuID'] = shiny.item.menu.id
        kwargs['appName'] = shiny.name
        kwargs['form'] = FShinyApp(instance=shiny, item=shiny.item.id)
        self.page_title = shiny.name+"-編輯"
        return super(CAppEdit, self).post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            shiny = ShinyApp.objects.get(id=request.POST.get('appID'))
            item = shiny.item
            dir = str(request.POST.get('dirName')).replace(" ","-")
            orgDir = shiny.dirName
            orgName = shiny.name
            config = Setting.objects.get(name="dirPath")
        except:
            return redirect(reverse('main:main'))
        
        form = FShinyApp(request.POST, instance=shiny)
        if not form.is_valid():
            kwargs['form'] = form
            kwargs['appID'] = shiny.id
            kwargs['menuID'] = shiny.item.menu.id
            return super(CAppAdd, self).post(request, *args, **kwargs)
        
        if orgDir != dir:
            os.rename(config.c1+orgDir, config.c1+dir)
        
        if 'upload_file' in request.FILES:
            file = request.FILES['upload_file']
            if os.path.exists(config.c1+dir):
                shutil.rmtree(config.c1+dir)
                
            os.makedirs(config.c1+dir)
            zip_ref = zipfile.ZipFile(file, 'r')
            zip_ref.extractall(config.c1+dir)
            zip_ref.close()
            
            os.makedirs(config.c1+dir+"/zip/")
            fd = open(config.c1+dir+'/zip/'+file.name, 'wb')
            for chunk in file.chunks():
                fd.write(chunk)
            fd.close()
            
            shiny.dirName = dir
            shiny.fileName = file.name
            shiny.fileType = file.content_type
            shiny.save()
            
        form.user = request.user
        form.save()
        
        shiny = ShinyApp.objects.filter(item=item)
        item.appQty = len(shiny)
        item.activeQty = len(shiny.filter(isActive=True))
        item.isActive = True if item.activeQty > 0 else False
        item.save()
        
        #messages.success(request, 'APP更新成功。')
        msg = "%s(%s) APP修改成功。" % (request.POST.get('name'), orgName)
        messages.success(request, msg)
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
            shiny.delete()
            #messages.success(request, shinyName+'刪除成功。')
            messages.success(request, shinyName+'刪除成功。')
        except Exception as e:
            #messages.success(request, shinyName+'刪除失敗。')
            messages.error(request, shinyName+'刪除失敗。')
            print(e)
        return redirect(reverse('control:apps', args=(itemID,)))
  
class CConfig(AdminBase):
    template_name = 'config/config.html' # xxxx/xxx.html
    page_title = '設定' # title

    def get(self, request, *args, **kwargs):
        return super(CConfig, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super(CConfig, self).post(request, *args, **kwargs)
    
class CConfigShiny(AdminBase):
    template_name = 'config/dir.html' # xxxx/xxx.html
    page_title = '設定' # title
    
    def get(self, request, *args, **kwargs):
        try:
            config = Setting.objects.get(name="dirPath")
            kwargs['path'] = config.c1
            kwargs['time'] = config.time
        except Exception as e:
            print(e)
        return super(CConfigShiny, self).post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if 'dirPath' not in request.POST:
            kwargs['error'] = "請輸入路徑"
            return super(CConfigShiny, self).post(request, *args, **kwargs)
        
        dir = request.POST.get('dirPath')
        
        if not os.path.exists(dir):
            kwargs['error'] = " *路徑錯誤"
            kwargs['path'] = dir
            return super(CConfigShiny, self).post(request, *args, **kwargs)
        
        try:
            config = Setting.objects.get(name="dirPath")
            config.c1 = dir
            config.save()
        except Exception as e:
            Setting.objects.get_or_create(name="dirPath",c1=dir)
            print(e)
        
        #messages.success(request, "設定成功。")
        messages.success(request,"設定成功。")
        return redirect(reverse('control:configAPP'))


class CConfigSchoolAPI(AdminBase):
    template_name = 'config/api.html' # xxxx/xxx.html
    page_title = '學校 API 設定' # title

    def get(self, request, *args, **kwargs):
        try:
            config = Setting.objects.get(name="SchoolAPI")
            kwargs['isActive'] = config.isActive
            kwargs['url'] = config.c1
            kwargs['time'] = config.time
        except Exception as e:
            print(e)
        return super(CConfigSchoolAPI, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('apiURL')=="":
            kwargs['error'] = "*URL 不能為空"
            return super(CConfigSchoolAPI, self).post(request, *args, **kwargs)
        
        try:
            config = Setting.objects.get(name="SchoolAPI")
            config.c1 = request.POST.get('apiURL')
            config.isActive = True if request.POST.get('isActive') else False
            config.save()
        except Exception as e:
            Setting.objects.get_or_create(name="SchoolAPI",isActive = True if request.POST.get('isActive') else False, c1 = request.POST.get('apiURL'))
            print(e)
        #messages.success(request, "設定成功。")
        messages.success(request, "設定成功。")
        return redirect(reverse('control:configAPI'))
    
class CCongigKey(AdminBase):
    template_name = 'config/key.html' # xxxx/xxx.html
    page_title = '系統金鑰設定' # title

    def get(self, request, *args, **kwargs):
        try:
            config = Setting.objects.get(name="SystemKey")
            kwargs['key'] = config.c1
            kwargs['time'] = config.time
        except Exception as e:
            print(e)
        return super(CCongigKey, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('key')=="":
            kwargs['error'] = "*HOST 不能為空"
            return super(CCongigKey, self).post(request, *args, **kwargs)
        
        try:
            config = Setting.objects.get(name="SystemKey")
            config.c1 = request.POST.get('key')
            config.save()
        except Exception as e:
            Setting.objects.get_or_create(name="SystemKey", c1 = request.POST.get('key'))
            print(e)
        #messages.success(request, "設定成功。")
        messages.success(request, "設定成功。")
        return redirect(reverse('control:configKEY'))
    
    
    
class CMove(ManagerBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title
    
    def post(self, request, *args, **kwargs):
        move = None
        url = None
        type = request.POST.get('TYPE')
        up = int(request.POST.get('UP')) if request.POST.get('UP')!="" else None
        down = int(request.POST.get('DOWN')) if request.POST.get('DOWN')!="" else None
        target = up if up else down
        
        if type=="menu":
            move = Menu.objects.all().order_by("order")
            url = redirect(reverse('control:menu'))
        elif type=="item":
            tempMove = Item.objects.get(id=target)
            move = Item.objects.filter(menu=tempMove.menu).order_by("order")
            url = redirect(reverse('control:itemBy', args=(tempMove.menu.id,)))
        elif type=="apps":
            tempMove = ShinyApp.objects.get(id=target)
            move = ShinyApp.objects.filter(item=tempMove.item).order_by("order")
            url = redirect(reverse('control:apps', args=(tempMove.item.id,)))
            
        length = len(list(move))
        first = move[0]
        last = move[length-1]

        if first.id == up:
            #messages.success(request, first.name+' 已經在最上方。')
            messages.success(request, first.name+' 已經在最上方。')
            return url
        elif last.id==down:
            #messages.success(request, last.name+' 已經在最下方。')
            messages.success(request, first.name+' 已經在最下方。')
            return url

        if up:
            for i in range(1,length):
                if move[i].id==up:
                    tmp = move[i].order
                    move[i].order=move[i-1].order
                    move[i-1].order=move[i].order
                    move[i-1].order=tmp
                    move[i].save()
                    move[i-1].save()
                    #messages.success(request, move[i].name+' 成功向上移動。')
                    messages.success(request, move[i].name+' 成功向上移動。')
                    break
        elif down:
            for i in range(0,length-1):
                if move[i].id==down:
                    tmp = move[i].order
                    move[i].order=move[i+1].order
                    move[i+1].order=move[i].order
                    move[i+1].order=tmp
                    move[i].save()
                    move[i+1].save()
                    #messages.success(request, move[i].name+'成功向下移動。')
                    messages.success(request, move[i].name+' 成功向下移動。')
                    break
        return url
    
    
class CPermissions(AdminBase):
    template_name = 'permissions/permissions.html' # xxxx/xxx.html
    page_title = '權限管理' # title

    def get(self, request, *args, **kwargs):
        kwargs['group'] = DBGroupName.objects.all().iterator()
        return super(CPermissions, self).get(request, *args, **kwargs)
    
class CPermissionsAdd(AdminBase):
    template_name = 'permissions/add.html' # xxxx/xxx.html
    page_title = '新增權限類別' # title
    
    def get(self, request, *args, **kwargs):
        cgroup = ItemGroupManage(kwargs)
        cgroup.setList()
        return super(CPermissionsAdd, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        users = request.POST.getlist('users')
        items = request.POST.getlist('items')
        name = request.POST.get('name')
        cgroup = ItemGroupManage(kwargs)
        cgroup.setList()
        if cgroup.userValid(users) and cgroup.itemValid(items) and cgroup.create(name):
            messages.success(request, "新增 %s 群組成功。" % (name, ) )
            return redirect(reverse('control:permissions'))
        
        return super(CPermissionsAdd, self).get(request, *args, **kwargs)
        
class CPermissionsEdit(AdminBase):
    template_name = 'permissions/edit.html' # xxxx/xxx.html

    def get(self, request, *args, **kwargs):
        cgroup = ItemGroupManage(kwargs)
        cgroup.setList()
        if(not cgroup.setEditList()):
            return redirect(reverse('control:permissions'))
        self.page_title = kwargs['name']+" 群組權限編輯"

        return super(CPermissionsEdit, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        cgroup = ItemGroupManage(kwargs)
        cgroup.setList()
        if(not cgroup.setEditList()):
            return redirect(reverse('control:permissions'))
        self.page_title = kwargs['name']+" 群組權限編輯"
        users = request.POST.getlist('users')
        items = request.POST.getlist('items')
        name = request.POST.get('name')
        print(True)
        if cgroup.userValid(users) and cgroup.itemValid(items) and cgroup.save(name):
            messages.success(request, "新增 %s 編輯成功。" % (name, ) )
            return redirect(reverse('control:permissions'))
        return super(CPermissionsEdit, self).post(request, *args, **kwargs)
        
class CPermissionsDetail(AdminBase):
    template_name = 'permissions/detail.html' # xxxx/xxx.html

    def get(self, request, *args, **kwargs):
        cgroup = ItemGroupManage(kwargs)
        if not cgroup.getDetail():
            return redirect(reverse('control:permissions'))
        self.page_title = kwargs['group'].name+" 群組詳細資料"
        return super(CPermissionsDetail, self).get(request, *args, **kwargs)
    
class CPermissionsRemove(AdminBase):
    template_name = '' # xxxx/xxx.html
    page_title = ""
    def post(self, request, *args, **kwargs):
        print(request.POST.get('groupID'))
        print(request.POST.get('groupName'))
        try:
            group = DBGroupName.objects.get(id=request.POST.get('groupID'), name=request.POST.get('groupName'))
            name = group.name
            DBGroupItem.objects.filter(group=group).delete()
            group.delete()
            messages.success(request, "新增 %s 移除成功。" % (name, ))
        except Exception as e:
            messages.error(request, "移除權限失敗，資料不相符。")
            print(e)
        return redirect(reverse('control:permissions'))
        
class CAccount(AdminBase):
    template_name = 'account/account.html' # xxxx/xxx.html
    page_title = '帳號管理' # title

    def get(self, request, *args, **kwargs):
        account = AccountManage(kwargs)
        account.getUser()
        return super(CAccount, self).get(request, *args, **kwargs)

class CAccountAdd(AdminBase):
    template_name = 'account/add.html' # xxxx/xxx.html
    page_title = '加入帳號' # title
    
    def get(self, request, *args, **kwargs):
        kwargs['userForm'] = UserForm()
        kwargs['userProfileForm'] = UserProfileForm()
        return super(CAccountAdd, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        userForm = UserForm(request.POST)
        userProfileForm = UserProfileForm(request.POST)      
        if not (userForm.is_valid() and userProfileForm.is_valid()):
            kwargs['userForm'] = userForm
            kwargs['userProfileForm'] = userProfileForm
            return super(CAccountAdd, self).post(request, *args, **kwargs) 
        
        user = userForm.save()
        user.set_password(user.password)
        user.save()
        userProfile = userProfileForm.save(commit=False)
        userProfile.user = user
        userProfile.type=1 if 'isManager' in request.POST else 0 #0 = Normal #1 = Manager
        userProfile.isActive = False if 'isBan' in request.POST else True
        userProfile.isAuth = False
        userProfile.save()
        messages.success(request,user.username+' 帳號加入成功。')
        return redirect(reverse('control:account'))
    
class CAccountEdit(AdminBase):
    template_name = 'account/edit.html' # xxxx/xxx.html
    page_title = '編輯帳號' # titled
    
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['id'])
            kwargs['userForm'] = UserEditForm(instance=user)
            kwargs['userProfileForm'] = UserProfileForm(instance=user.profile)
            kwargs['account'] = user
        except Exception as e:
            print(e)
            return redirect(reverse('control:account'))
        
        return super(CAccountEdit, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['id'])
            username = user.username
        except Exception as e:
            print(e)
            return redirect(reverse('control:account'))
        
        
        userForm = UserEditForm(request.POST, instance=user)
        userProfileForm = UserProfileForm(request.POST, instance=user.profile)
        kwargs['userForm'] = userForm
        kwargs['userProfileForm'] = userProfileForm
        kwargs['account'] = user
        if not (userForm.is_valid() and userProfileForm.is_valid()):
            return super(CAccountEdit, self).post(request, *args, **kwargs)
        
        if(userForm.cleaned_data['username']!=username):
            kwargs['error'] = "帳號不能修改。"
            return super(CAccountEdit, self).post(request, *args, **kwargs)
        
        user = userForm.save()
        if(userForm.cleaned_data['password']!=""):
            user.set_password(userForm.cleaned_data['password'])
            user.save()
        userProfile = userProfileForm.save()
        userProfile.type=1 if 'isManager' in request.POST else 0 #0 = Normal #1 = Manager
        userProfile.isActive = False if 'isBan' in request.POST else True
        userProfile.save()
        messages.success(request,user.username+' 帳號修改成功。')
        return redirect(reverse('control:account'))
        
class CAccountRemove(AdminBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.POST.get('accountID'), username=request.POST.get('accountName'))
            if user.profile:
                user.profile.delete()
            user.delete()
            username = user.username
        except Exception as e:
            print(e)
            messages.error(request, "移除帳號失敗，資料不相符。")
            return redirect(reverse('control:account'))
        messages.success(request, username+" 移除帳號成功。")
        return redirect(reverse('control:account'))
    
class CAccountDetail(AdminBase):
    template_name = 'account/detail.html' # xxxx/xxx.html

    def get(self, request, *args, **kwargs):
        account = AccountManage(kwargs)
        if account.getUserDetail():
            self.page_title = kwargs['account'].username+' 帳號資料' # title
            return super(CAccountDetail, self).get(request, *args, **kwargs)
        return redirect(reverse('control:account'))
