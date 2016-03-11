import os, zipfile, shutil
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import JsonResponse
from main.views import BaseView, UserBase, LoginRequiredMixin
from main.models import Setting
from db.models import Demo
from .forms import DemoForm
# Create your views here.

class DeveloperBase(BaseView):
    base_template_name = 'developer/base.html'
    template_dir_name = "developer/"
    
    def __init__(self, *args, **kwargs):
        super(DeveloperBase, self).__init__(*args, **kwargs)
        self.page_title="開發者"+self.page_title
        self.template_name = self.template_dir_name+self.template_name


class DeveloperUserBase(DeveloperBase, LoginRequiredMixin):
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

        form = form.save(commit=False)
        try:
            config = Setting.objects.get(name="dirPath")
            
            if os.path.exists(config.c1+form.dirName):
                kwargs['dir_exists'] = "*資料夾已存在"
                kwargs['form'] = form
                return super(Upload, self).post(request, *args, **kwargs)
            
            file = request.FILES['upload_file']
            os.makedirs(config.c1+form.dirName)
            zip_ref = zipfile.ZipFile(file, 'r')
            zip_ref.extractall(config.c1+form.dirName)
            zip_ref.close()
        except Exception as e:
            print(e)
            kwargs['file_error'] = "*檔案格式錯誤"
            kwargs['form'] = form
            return super(Upload, self).post(request, *args, **kwargs)
        
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
        response = {}
        try:
            demoID = request.POST.get('demoID')
            demo = Demo.objects.get(id=demoID)
            config = Setting.objects.get(name="dirPath")
            if os.path.exists(config.c1+demo.dirName):
                shutil.rmtree("config.c1"+demo.dirName)
                demo.delete()
            response['status']="success"
        except Exception as e:
            response['status']="fail"
            print(e)
         
        return JsonResponse(response)
    
class Config(DeveloperUserBase):
    template_name = 'config/dir.html' # xxxx/xxx.html
    page_title = '設定' # title
    
    def get(self, request, *args, **kwargs):
        try:
            config = Setting.objects.get(name="dirPath")
            kwargs['path'] = config.c1
            kwargs['time'] = config.time
        except Exception as e:
            print(e)
        return super(Config, self).post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if 'dirPath' not in request.POST:
            kwargs['error'] = "請輸入路徑"
            return super(Config, self).post(request, *args, **kwargs)
        
        dir = request.POST.get('dirPath')
        
        if not os.path.exists(dir):
            kwargs['error'] = " *路徑錯誤"
            return super(Config, self).post(request, *args, **kwargs)
        
        try:
            config = Setting.objects.get(name="dirPath")
            config.c1 = dir
            config.save()
        except Exception as e:
            Setting.objects.get_or_create(name="dirPath",c1=dir)
            print(e)
        
        messages.success(request, "設定成功。")
        return redirect(reverse('developer:config'))

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
        
            
        return redirect(reverse('developer:school'))
     