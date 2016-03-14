import os, zipfile, shutil
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import JsonResponse
from main.views import BaseView, UserBase
from main.models import Setting
from db.models import Demo
from .forms import DemoForm
# Create your views here.

def developer_required(fun):
    def auth(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(settings.LOGIN_URL +'?next=%s' % request.path)
        if request.user.detail.type < 2:
            return redirect(reverse('main:main'))
        return fun(request, *args, **kwargs)
    return auth

class DeveloperRequiredMixin(object):
    @classmethod
    def as_view(self):
        return developer_required(super(DeveloperRequiredMixin, self).as_view())

class DeveloperBase(DeveloperRequiredMixin, BaseView):
    base_template_name = 'developer/base.html'
    template_dir_name = "developer/"
    
    def __init__(self, *args, **kwargs):
        super(DeveloperBase, self).__init__(*args, **kwargs)
        
        self.page_title="開發者"+self.page_title
        self.template_name = self.template_dir_name+self.template_name


class DeveloperUserBase(DeveloperBase):
    def __init__(self, *args, **kwargs):
        super(DeveloperUserBase, self).__init__(*args, **kwargs)
        

class Main(DeveloperBase):
    template_name = 'main.html' # xxxx/xxx.html
    page_title = '首頁' # title


class Uplist(DeveloperBase):
    template_name = 'list.html' # xxxx/xxx.html
    page_title = '已上傳列表' # title

    def get(self, request, *args, **kwargs):
        demo = Demo.objects.all()
        kwargs['demo'] = demo
        return super(Uplist, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super(Uplist, self).post(request, *args, **kwargs)

class Upload(DeveloperUserBase):
    template_name = 'upload.html' # xxxx/xxx.html
    page_title = '檔案上傳' # title

    def get(self, request, *args, **kwargs):
        kwargs['form'] = DemoForm()
        return super(Upload, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        
        form = DemoForm(request.POST)
        if not form.is_valid():
            kwargs['form'] = form
            return super(Upload, self).post(request, *args, **kwargs)
        if 'upload_file' not in request.FILES:
            kwargs['not_found']="*請選擇檔案"
            kwargs['form'] = form
            return super(Upload, self).post(request, *args, **kwargs)
        
        try:
            config = Setting.objects.get(name="dirPath")
            dirName = request.POST.get('dirName')
            if os.path.exists(config.c1+dirName):
                kwargs['dir_exists'] = "* 資料夾已存在"
                kwargs['form'] = form
                return super(Upload, self).post(request, *args, **kwargs)
            
            file = request.FILES['upload_file']
            os.makedirs(config.c1+dirName)
            zip_ref = zipfile.ZipFile(file, 'r')
            zip_ref.extractall(config.c1+dirName)
            zip_ref.close()
        except Exception as e:
            print(e)
            kwargs['file_error'] = "*檔案格式錯誤"
            kwargs['form'] = form
            return super(Upload, self).post(request, *args, **kwargs)
        
        form = form.save(commit=False)
        form.user = request.user
        form.save()
        messages.success(request, '上傳成功')
        return redirect(reverse('developer:main'))


class Remove(DeveloperUserBase):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title

    def get(self, request, *args, **kwargs):
        return redirect('main:main')
    
    def post(self, request, *args, **kwargs):
        try:
            demoID = request.POST.get('demoID')
            demo = Demo.objects.get(id=demoID)
            
            if demo.user.username != request.user.username and request.user.detail.type<=2:
                messages.success(request, demo.name+'刪除失敗，權限不足。')
                return redirect(reverse('developer:list'))
            
            config = Setting.objects.get(name="dirPath")
            if os.path.exists(config.c1+demo.dirName):
                shutil.rmtree(config.c1+demo.dirName)
                demo.delete()
            messages.success(request, demo.name+'刪除成功。')
        except Exception as e:
            messages.success(request, demo.name+'刪除失敗。')
            print(e)
         
        return redirect(reverse('developer:list'))
    
class Config(DeveloperUserBase):
    template_name = 'config/config.html' # xxxx/xxx.html
    page_title = '設定列表' # title
    
    def get(self, request, *args, **kwargs):
        return super(Config, self).post(request, *args, **kwargs)

class ConfigShiny(DeveloperUserBase):
    template_name = 'config/dir.html' # xxxx/xxx.html
    page_title = '設定' # title
    
    def get(self, request, *args, **kwargs):
        try:
            config = Setting.objects.get(name="dirPath")
            kwargs['path'] = config.c1
            kwargs['time'] = config.time
        except Exception as e:
            print(e)
        return super(ConfigShiny, self).post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if 'dirPath' not in request.POST:
            kwargs['error'] = "請輸入路徑"
            return super(ConfigShiny, self).post(request, *args, **kwargs)
        
        dir = request.POST.get('dirPath')
        
        if not os.path.exists(dir):
            kwargs['error'] = " *路徑錯誤"
            kwargs['path'] = dir
            return super(ConfigShiny, self).post(request, *args, **kwargs)
        
        try:
            config = Setting.objects.get(name="dirPath")
            config.c1 = dir
            config.save()
        except Exception as e:
            Setting.objects.get_or_create(name="dirPath",c1=dir)
            print(e)
        
        messages.success(request, "設定成功。")
        return redirect(reverse('developer:configShiny'))


class ConfigSchoolAPI(DeveloperUserBase):
    template_name = 'config/school.html' # xxxx/xxx.html
    page_title = '啟用SchoolAPI' # title

    def get(self, request, *args, **kwargs):
        try:
            config = Setting.objects.get(name="SchoolAPI")
            kwargs['isActive'] = config.isActive
            kwargs['url'] = config.c1
            kwargs['time'] = config.time
        except Exception as e:
            print(e)
        return super(ConfigSchoolAPI, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('apiURL')=="":
            kwargs['error'] = "*URL 不能為空"
            return super(ConfigSchoolAPI, self).post(request, *args, **kwargs)
        
        try:
            config = Setting.objects.get(name="SchoolAPI")
            config.c1 = request.POST.get('apiURL')
            config.isActive = True if request.POST.get('isActive') else False
            config.save()
        except Exception as e:
            Setting.objects.get_or_create(name="SchoolAPI",isActive = True if request.POST.get('isActive') else False, c1 = request.POST.get('apiURL'))
            print(e)
        return redirect(reverse('developer:configAPI'))
    
class ConfigShinyHost(DeveloperUserBase):
    template_name = 'config/server.html' # xxxx/xxx.html
    page_title = 'Shiny Host' # title

    def get(self, request, *args, **kwargs):
        try:
            config = Setting.objects.get(name="ShinyHost")
            kwargs['host'] = config.c1
            kwargs['time'] = config.time
        except Exception as e:
            print(e)
        return super(ConfigShinyHost, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('host')=="":
            kwargs['error'] = "*HOST 不能為空"
            return super(ConfigShinyHost, self).post(request, *args, **kwargs)
        
        try:
            config = Setting.objects.get(name="ShinyHost")
            config.c1 = request.POST.get('host')
            config.save()
        except Exception as e:
            Setting.objects.get_or_create(name="ShinyHost", c1 = request.POST.get('host'))
            print(e)
        return redirect(reverse('developer:configShinyHost'))
     
class CongigKey(DeveloperUserBase):
    template_name = 'config/key.html' # xxxx/xxx.html
    page_title = '系統金鑰設定' # title

    def get(self, request, *args, **kwargs):
        try:
            config = Setting.objects.get(name="SystemKey")
            kwargs['key'] = config.c1
            kwargs['time'] = config.time
        except Exception as e:
            print(e)
        return super(CongigKey, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('key')=="":
            kwargs['error'] = "*HOST 不能為空"
            return super(CongigKey, self).post(request, *args, **kwargs)
        
        try:
            config = Setting.objects.get(name="SystemKey")
            config.c1 = request.POST.get('key')
            config.save()
        except Exception as e:
            Setting.objects.get_or_create(name="SystemKey", c1 = request.POST.get('key'))
            print(e)
        return redirect(reverse('developer:configKey'))
    
    
    