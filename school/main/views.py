import random
import string
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView
from django.conf import settings
from .models import Menu, Item, ShinyApp, DBGroupItem
from func.aescipher import AESCipher as ase
from func.aescipher import toSHA as sha1
from main.models import DBGroupUser, Setting

# Create your views here.

class BaseView(TemplateView):

    SITE_VERSION = ""
    # Base template to extend in drived views
    base_template_name = 'main/base.html'
    
    def __init__(self):
        if BaseView.SITE_VERSION != "":
            return
        
        data = Setting.objects.filter(name="SITE_VERSION")
        if(len(data) == 0):
            BaseView.SITE_VERSION = "unknow"
        else:
            BaseView.SITE_VERSION = data[0].c1
        print("BaseView initialize")
    
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)

        # Settings context data for base template
        context['base_template_name'] = self.base_template_name
        context['SITE_NAME'] = settings.SITE_NAME
        context['SITE_VERSION'] = BaseView.SITE_VERSION
        context['menu'] = Menu.objects.all().order_by('order')
        if hasattr(self, 'page_title'):
            context['page_title'] = self.page_title
        return context
    
    def get(self, request, *args, **kwargs):
        kwargs['serverIP'] = self.getHost(request)
        return super(BaseView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        kwargs['serverIP'] = self.getHost(request)
        return super(BaseView, self).get(request, *args, **kwargs)

    def getHost(self, request):
        if ":" in str(request.META['HTTP_HOST']):
            return str(request.META['HTTP_HOST']).split(":")[0]
        return str(request.META['HTTP_HOST'])
    
    def getPost(self, request):
        return request.META['SERVER_PORT']

def login_required(fun):
    def auth(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(settings.LOGIN_URL +'?next=%s' % request.path)
        if not request.user.profile.isActive:
            logout(request)
            return redirect(reverse('main:main'))
        return fun(request, *args, **kwargs)
    return auth

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())
    
class UserBase(LoginRequiredMixin,BaseView):
    def __init__(self, *args, **kwargs):
        super(UserBase, self).__init__(*args, **kwargs)


# Start 

class Index(BaseView):
    template_name = 'main/index.html' # xxxx/xxx.html
    page_title = '首頁' # title

    def get(self, request, *args, **kwargs):
        return super(Index, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super(Index, self).post(request, *args, **kwargs)

class CShinyApp(UserBase):
    template_name = 'main/shinyapp.html' # xxxx/xxx.html
    page_title = '???' # title

    def get(self, request, *args, **kwargs):
        try:
            itemID = kwargs['itemID'] if 'itemID' in kwargs else None
            item = Item.objects.get(id=itemID)
            shiny = ShinyApp.objects.filter(item=item, isActive=True).order_by("order")
            kwargs['menuID'] = item.menu.id 
        except Exception as e:
            print(e)
            return super(CShinyApp, self).get(request, *args, **kwargs)
        
        try:
            appID = kwargs['appID'] if 'appID' in kwargs else None
            app = ShinyApp.objects.get(id=appID)
            kwargs['shinyApp'] = app 
        except Exception as e:
            print(e)
            kwargs['shinyApp'] = shiny[0] 
        
        
        if len(shiny)==0:
            return super(CShinyApp, self).get(request, *args, **kwargs)
            
        if timezone.now() > request.user.profile.expire:
            request.user.profile.license = sha1(self.createCode(32)+request.user.password+request.user.username)
            request.user.profile.save()
        self.page_title=shiny[0].name

        kwargs['license'] = request.user.profile.license
        kwargs['shiny'] = shiny

        #權限處理
        user = request.user
        if user.profile.type>=1:
            kwargs['token'] = True
            return super(CShinyApp, self).get(request, *args, **kwargs)
        
        kwargs['token'] = self.getItemArr(item, user)
        return super(CShinyApp, self).get(request, *args, **kwargs)

    def createCode(self, num):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(num))
    
    def hasToken(self,item, user):
        itemArr = []
        for i in DBGroupUser.objects.filter(user=user):
            for j in DBGroupItem.objects.filter(group=i.group):
                itemArr.append(j.item.id)
        if user.profile.level > 0:
            for i in DBGroupItem.objects.filter(group=user.profile.adAdmin):
                itemArr.append(i.item.id)
            for i in DBGroupItem.objects.filter(group=user.profile.adAdmin2):
                itemArr.append(i.item.id)
            for i in DBGroupItem.objects.filter(group=user.profile.atAdmin):
                itemArr.append(i.item.id)
            for i in DBGroupItem.objects.filter(group=user.profile.atAdmin2):
                itemArr.append(i.item.id)
        return True if item.id in itemArr else False

def blank(request):
    return HttpResponse("Page not found.")