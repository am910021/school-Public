from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from account.forms import UserForm, UserProfileForm
from main.views import BaseView


class Login(BaseView):
    template_name = 'account/login.html' # xxxx/xxx.html
    page_title = '登入' # title

    def get(self, request, *args, **kwargs):
        if request.user.username!="":
            messages.success(request, '登入成功')
            return redirect(reverse('main:main'))
        
        return super(Login, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        nextPage = request.POST.get('next')
        if not user: # authenticate fail
            kwargs['error'] = '登入失敗'
            kwargs['username'] = username
            kwargs['nextPage'] = nextPage
            return super(Login, self).post(request, *args, **kwargs)
        if not user.is_active:
            kwargs['error'] = '帳號已停用'
            return super(Login, self).post(request, *args, **kwargs)
        # login success
        login(request, user)
        messages.success(request, '登入成功')
        return redirect(nextPage if nextPage else reverse('main:main'))
        
class SignUp(BaseView):
    template_name = 'account/signup.html' # xxxx/xxx.html
    page_title = '註冊' # title

    def get(self, request, *args, **kwargs):
        kwargs['userForm'] = UserForm()
        kwargs['userProfileForm'] = UserProfileForm()
        return super(SignUp, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        userForm = UserForm(request.POST)
        userProfileForm = UserProfileForm(request.POST)
        if request.POST.get('betacode')!="Ew0Xav08L4":
            kwargs['error'] = "* 註冊碼錯誤"
            kwargs['userForm'] = userForm
            kwargs['userProfileForm'] = userProfileForm
            return super(SignUp, self).post(request, *args, **kwargs)
        
        if not (userForm.is_valid() and userProfileForm.is_valid()):
            kwargs['userForm'] = userForm
            kwargs['userProfileForm'] = userProfileForm
            return super(SignUp, self).post(request, *args, **kwargs)
        
        user = userForm.save()
        user.set_password(user.password)
        user.save()
        userProfile = userProfileForm.save(commit=False)
        userProfile.user = user
        userProfile.type=2 #2 = Developer
        userProfile.save()
        messages.success(request, '註冊成功')
        return redirect(reverse('main:main'))

def Logout(request):
    logout(request)
    messages.success(request, '歡迎再度光臨')
    return redirect(reverse('main:main'))