import random
import string
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import JsonResponse
from main.views import BaseView, UserBase
from main.models import Setting
from func.aescipher import toSHA as sha1
# Create your views here.

def developer_required(fun):
    def auth(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(settings.LOGIN_URL +'?next=%s' % request.path)
        if request.user.profile.type < 1:
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
        #self.context['demomenu'] = Demo.objects.all()
        self.page_title="開發者"+self.page_title
        self.template_name = self.template_dir_name+self.template_name
        
    def get(self, request, *args, **kwargs):
        return super(DeveloperBase, self).get(request, *args, **kwargs)

class Main(DeveloperBase):
    template_name = 'main.html' # xxxx/xxx.html
    page_title = '首頁' # title
    def get(self, request, *args, **kwargs):
        if timezone.now() > request.user.profile.expire:
            request.user.profile.license = sha1(self.createCode(32)+request.user.password+request.user.username)
            request.user.profile.save()
        kwargs['license'] = request.user.profile.license
        kwargs['expire']= request.user.profile.expire
        return super(Main, self).get(request, *args, **kwargs)
    
    def createCode(self, num):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(num))
    
