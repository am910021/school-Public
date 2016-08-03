from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django import forms
from bs4 import BeautifulSoup
import requests as requests
from account.models import Profile
from account.forms import UserForm, UserProfileForm
from main.views import BaseView, UserBase
from main.models import DBGroupItem, DBGroupName


class Login(BaseView):
    template_name = 'account/login.html' # xxxx/xxx.html
    page_title = '登入' # title

    def get(self, request, *args, **kwargs):
        if request.user.username!="":
            #messages.success(request, '登入成功')
            messages.success(request,request.user.username+'會員登入成功')
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
        if not user.profile.isActive:
            kwargs['error'] = '帳號已停用。'
            return super(Login, self).post(request, *args, **kwargs)
        if user.profile.isAuth:
            kwargs['error'] = '此帳號為第三方認證帳戶，無法登入。'
            return super(Login, self).post(request, *args, **kwargs)
        
        # login success
        login(request, user)
        #messages.success(request, '登入成功')
        messages.success(request,request.user.username+'會員登入成功')
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
        userProfile.type=1 #2 = Manager
        userProfile.save()
        #messages.success(request, '註冊成功')
        messages.success(request,'註冊成功')
        return redirect(reverse('main:main'))

def Logout(request):
    logout(request)
    #messages.success(request, '歡迎再度光臨')
    messages.success(request, '歡迎再度光臨')
    return redirect(reverse('main:main'))


class CCenter(UserBase):
    template_name = 'account/center.html' # xxxx/xxx.html
    page_title = '帳戶中心' # title
    
class CModify(UserBase):
    template_name = 'account/modify.html' # xxxx/xxx.html
    page_title = '修改資料' # title
    
    def get(self, request, *args, **kwargs):
        if(request.user.profile.isAuth):
            return redirect(reverse('account:center'))
        
        
        kwargs['name'] = request.user.profile.fullName
        kwargs['email'] = request.user.email
        return super(CModify, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        kwargs['name'] = name
        kwargs['email'] = email
        error = False
        if(name==""):
            kwargs['name_error'] = "* 使用者全名不能留空。"
            error = True
        try:
            validate_email(request.POST.get("email", ""))
        except forms.ValidationError as e:
            kwargs['email_error'] = "* 輸入有效的電子郵件地址。"
            error = True
        if(not authenticate(username=request.user.username, password=password)):
            kwargs['password_error'] = "* 密碼錯誤，請重新輸入。"
            error = True
        if error:
            return super(CModify, self).post(request, *args, **kwargs)
        
        user = request.user
        user.email = email
        user.profile.fullName=name
        user.profile.save()
        user.save()
        messages.success(request,request.user.username+' 帳戶資料修改成功。')
        return redirect(reverse('account:center'))
    
    
class CModifyPwd(UserBase):
    template_name = 'account/modify_pwd.html' # xxxx/xxx.html
    page_title = '修改密碼' # title
    
    def get(self, request, *args, **kwargs):
        if(request.user.profile.isAuth):
            return redirect(reverse('account:center'))
        return super(CModifyPwd, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        orgPwd = request.POST.get('password')
        newPwd = request.POST.get('newPwd')
        newPwd2 = request.POST.get('newPwd2')
        error = False
        if(not authenticate(username=request.user.username, password=orgPwd)):
            kwargs['password_error'] = "* 密碼錯誤，請重新輸入。"
            error = True
        if(newPwd==""):
            kwargs['newPwd_error'] = "* 新密碼不能留空。"   
            error = True
        if(newPwd2==""):
            kwargs['newPwd2_error'] = "* 確認密碼不能留空。"   
            error = True
        if(newPwd2!=newPwd):
            kwargs['newPwd2_error'] = "* 確認密碼錯誤。"   
            error = True
        user = request.user
        user.set_password(newPwd)
        user.save()
            
            
        if error:
            return super(CModifyPwd, self).post(request, *args, **kwargs)
        messages.success(request,request.user.username+' 帳戶密碼修改成功，麻煩請重新登入。')
        return redirect(reverse('account:center'))

class CPermissions(UserBase):
    template_name = 'account/permissions.html' # xxxx/xxx.html
    page_title = '權限資料' # title

    def get(self, request, *args, **kwargs):
        group = request.user.profile.group
        kwargs['items'] = DBGroupItem.objects.filter(group=group)
        kwargs['group'] = group
        
        return super(CPermissions, self).get(request, *args, **kwargs)
    
class CAccountAuth(BaseView):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title

    def get(self, request, *args, **kwargs):
        token = kwargs['token']
        if len(token)!=64:
            return HttpResponse('第三方驗證錯誤無法使用.')
        try:
            res=requests.get("https://admin.cyut.edu.tw/interface/Auth.aspx?s=%s&c=%s" % ("yhImR", token))
        except Exception as e:
            print(e)
            return HttpResponse('第三方驗證錯誤無法使用.')
        root = BeautifulSoup(res.text,"lxml").select('root')
        if len(root)==0:
            return HttpResponse('第三方驗證錯誤無法使用.')
        if len(root[0].select('msg'))>0:
            return HttpResponse('第三方驗證錯誤無法使用.')
        
        root = root[0]
        id = root.select('id')[0].text
        name = root.select('name')[0].text
        other = root.select('other')[0].text if len(root.select('other'))>0 else None
        
        user = User.objects.filter(username=id)
        if len(user)==1 and user[0].profile.isAuth and user[0].profile.isActive:
            user = user[0]
            user.profile.fullName = name
            user.profile.save()
            login(request, authenticate(username=user.username, password=user.username))
            messages.success(request,request.user.username+'帳號認證成功。')
        elif len(user)==0:
            newUser = User()
            newUser.username = id
            newUser.set_password(id)
            newUser.save()
            profile = Profile()
            profile.user = newUser
            profile.fullName = name
            profile.type=0
            profile.isActive=True
            profile.isAuth=True
            profile.save()
            messages.success(request,request.user.username+'帳號認證成功。')
            login(request, authenticate(username=id, password=id))
        else:
            messages.error(request,'帳號認證失敗。')
        return redirect(reverse('main:main'))
    
    def post(self, request, *args, **kwargs):
        return redirect(reverse('main:main'))
    