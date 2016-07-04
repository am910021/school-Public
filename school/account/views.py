from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django import forms
from account.forms import UserForm, UserProfileForm
from main.views import BaseView, UserBase
from main.models import DBItemGroups, DBItemGroupName


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
    page_title = '權限群組查尋' # title

    def get(self, request, *args, **kwargs):
        group = []
        for i in DBItemGroups.objects.filter(user=request.user).values_list('group', flat=True).distinct():
            group.append(DBItemGroupName.objects.get(id=i))
        kwargs['group'] = group
        return super(CPermissions, self).get(request, *args, **kwargs)

class CPermissionsDetail(UserBase):
    template_name = 'account/permissions_detail.html' # xxxx/xxx.html

    def get(self, request, *args, **kwargs):
        try:
            group = DBItemGroupName.objects.get(id=kwargs['id'])
        except Exception as e:
            print(e)
            return redirect(reverse('account:permissions'))

        self.page_title = group.name+'群組資料'
        kwargs['items'] = DBItemGroups.objects.filter(user=request.user, group=group)
        kwargs['groupName'] = group.name
        return super(CPermissionsDetail, self).get(request, *args, **kwargs)


