import random
import string
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required 
from django.conf import settings
from db.models import Demo
from .aescipher import AESCipher as ase
from .aescipher import toSHA as sha1

# Create your views here.

class BaseView(TemplateView):

    # Base template to extend in drived views
    base_template_name = 'main/base.html'

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
            
        # Settings context data for base template
        context['base_template_name'] = self.base_template_name
        context['SITE_NAME'] = settings.SITE_NAME
        context['demo'] = Demo.objects.all()
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
        return str(request.META['HTTP_HOST']).split(":")[0]
    
    def getPost(self, request):
        return request.META['SERVER_PORT']

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
    page_title = '校物系統首頁' # title

    def get(self, request, *args, **kwargs):
        return super(Index, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super(Index, self).post(request, *args, **kwargs)

class ShowDemo(UserBase):
    template_name = 'main/demo.html' # xxxx/xxx.html
    page_title = 'Demo 展示' # title

    def get(self, request, *args, **kwargs):
        if 'demoID' not in kwargs:
            return super(ShowDemo, self).get(request, *args, **kwargs)

        chart_demo = None
        try:
            chart_demo = Demo.objects.get(id=kwargs['demoID'])
        except Exception as e:
            print(e)
            
        
        
        if timezone.now() > request.user.detail.expire:
            request.user.detail.license = sha1(self.createCode(32)+request.user.password+request.user.username)
            request.user.detail.save()
        kwargs['license'] = request.user.detail.license
        kwargs['chart_demo'] = chart_demo
        

        return super(ShowDemo, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super(ShowDemo, self).post(request, *args, **kwargs)
    
    def createCode(self, num):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(num))


