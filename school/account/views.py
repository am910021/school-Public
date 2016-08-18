from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django import forms
from bs4 import BeautifulSoup
import requests as requests
from account.models import Profile
from account.forms import UserForm, UserProfileForm
from main.views import BaseView, UserBase
from main.models import DBGroupItem, DBGroupName, DBGroupUser


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
        itemArr = []
        user = request.user
        if user.profile.level==0:
            for i in DBGroupUser.objects.filter(user=user):
                for j in DBGroupItem.objects.filter(group=i.group):
                    itemArr.append(j)
        elif user.profile.level > 0:
            for i in DBGroupItem.objects.filter(group=user.profile.adAdmin):
                itemArr.append(i)
            for i in DBGroupItem.objects.filter(group=user.profile.adAdmin2):
                itemArr.append(i)
            for i in DBGroupItem.objects.filter(group=user.profile.atAdmin):
                itemArr.append(i)
            for i in DBGroupItem.objects.filter(group=user.profile.atAdmin2):
                itemArr.append(i)
        
        kwargs['items'] = itemArr
        kwargs['itemQty'] = len(itemArr)
        
        return super(CPermissions, self).get(request, *args, **kwargs)
    
class CAccountAuth(BaseView):
    template_name = '' # xxxx/xxx.html
    page_title = '' # title

    def get(self, request, *args, **kwargs):
        if self.Auth( request, *args, **kwargs):
            return redirect(reverse('main:main'))
        return HttpResponse('第三方驗證錯誤無法使用.')
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if self.Auth( request, *args, **kwargs):
            return redirect(reverse('main:main'))
        return HttpResponse('第三方驗證錯誤無法使用.')
    
    
    def Auth(self, request, *args, **kwargs):
        token = kwargs['token']
        token = token[:len(token)-1]
        if len(token)!=64:
            return False
        try:
            res=requests.get("https://admin.cyut.edu.tw/interface/Auth.aspx?s=%s&c=%s" % ("yhImR", token))
        except Exception as e:
            print(e)
            return False
        root = BeautifulSoup(res.text,"lxml").select('root')
        if len(root)==0:
            return False
        if len(root[0].select('msg'))>0:
            return False
        
        root = root[0]
        id = root.select('id')[0].text
        name = root.select('name')[0].text
        
        
        user = User.objects.filter(username=id)
        if len(user)==1 and user[0].profile.isAuth and user[0].profile.isActive:
            user = user[0]
            user.profile.fullName = name
            user.profile.save()
            self.isAdmin(root,user.profile)
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
            self.isAdmin(root,profile)
            login(request, authenticate(username=id, password=id))
            messages.success(request,newUser.username+'帳號認證成功。')
        else:
            return False
        return True
    
    
    def isAdmin(self, xml, profile):
        ad_iscoladmin = True if xml.select('ad_iscoladmin')[0].text=="True" else False
        ad_isdepadmin = True if xml.select('ad_isdepadmin')[0].text=="True" else False
        ad_iscoladmin2 = True if xml.select('ad_iscoladmin2')[0].text=="True" else False
        ad_isdepadmin2 = True if xml.select('ad_isdepadmin2')[0].text=="True" else False
        at_iscoladmin = True if xml.select('at_iscoladmin')[0].text=="True" else False
        at_isdepadmin = True if xml.select('at_isdepadmin')[0].text=="True" else False
        at_iscoladmin2 = True if xml.select('at_iscoladmin2')[0].text=="True" else False
        at_isdepadmin2 = True if xml.select('at_isdepadmin2')[0].text=="True" else False
        adAdmin = None
        adAdmin2 = None
        atAdmin = None
        atAdmin2 = None
        ad_adminCode = None
        ad_adminName = None
        ad_adminCode2 = None
        ad_adminName2 = None
        at_adminCode = None
        at_adminName = None
        at_adminCode2 = None
        at_adminName2 = None
        level = 0
        
        if ad_iscoladmin:
            ad_adminCode = xml.select('ad_colno')[0].text
            ad_adminName = xml.select('ad_colname')[0].text
            level=1
            print("ad_iscoladmin")
        elif ad_isdepadmin:
            ad_adminCode = xml.select('ad_depno')[0].text
            ad_adminName = xml.select('ad_depname')[0].text
            level=2 if level!=1 else 1
            print("ad_isdepadmin")
        if ad_adminCode:
            if len(DBGroupName.objects.filter(code=ad_adminCode))==0:
                adAdmin = DBGroupName.objects.create(code=ad_adminCode, name=ad_adminName, level=1)
            else:
                adAdmin = DBGroupName.objects.get(code=ad_adminCode)
            
        
        if ad_iscoladmin2:
            ad_adminCode2 = xml.select('ad_colno2')[0].text
            ad_adminName2 = xml.select('ad_colname2')[0].text
            level=1
            print("ad_iscoladmin2")
        elif ad_isdepadmin2:
            ad_adminCode2 = xml.select('ad_depno2')[0].text
            ad_adminName2 = xml.select('ad_depname2')[0].text
            level=2 if level!=1 else 1
            print("ad_isdepadmin2")
        if ad_adminCode2:
            if len(DBGroupName.objects.filter(code=ad_adminCode2))==0:
                adAdmin2 = DBGroupName.objects.create(code=ad_adminCode2, name=ad_adminName2, level=2)
            else:
                adAdmin2 = DBGroupName.objects.get(code=ad_adminCode2)
            
            
        if at_iscoladmin:
            at_adminCode = xml.select('at_colno')[0].text
            at_adminName = xml.select('at_colname')[0].text
            level=1
            print("at_iscoladmin")
        elif at_isdepadmin:
            at_adminCode = xml.select('at_depno')[0].text
            at_adminName = xml.select('at_depname')[0].text
            level=2 if level!=1 else 1
            print("at_isdepadmin")
        if at_adminCode:
            if len(DBGroupName.objects.filter(code=at_adminCode))==0:
                atAdmin = DBGroupName.objects.create(code=at_adminCode, name=at_adminName, level=1)
            else:
                atAdmin = DBGroupName.objects.get(code=at_adminCode)
            
            
        if at_iscoladmin2:
            at_adminCode2 = xml.select('at_colno2')[0].text
            at_adminName2 = xml.select('at_colname2')[0].text
            level=1
            print("at_iscoladmin2")
        elif at_isdepadmin2:
            at_adminCode2 = xml.select('at_depno2')[0].text
            at_adminName2 = xml.select('at_depname2')[0].text
            level=2 if level!=1 else 1
            print("at_isdepadmin2")
        if at_adminCode2:
            if len(DBGroupName.objects.filter(code=at_adminCode2))==0:
                atAdmin2 = DBGroupName.objects.create(code=at_adminCode2, name=at_adminName2, level=2)
            else:
                atAdmin2 = DBGroupName.objects.get(code=at_adminCode2)
            
            
            
        if adAdmin:
            print('adAdmin')
        if adAdmin2:
            print('adAdmin2') 
        if atAdmin:
            print('atAdmin')
        if atAdmin2:
            print('atAdmin2')
            
        profile.adAdmin = adAdmin
        profile.adAdmin2 = adAdmin2
        profile.atAdmin = atAdmin
        profile.atAdmin2 = atAdmin2
        profile.level = level
        profile.save()
        
    