from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from account.forms import UserForm, UserProfileForm

def Login(request):
    template = 'account/login.html'
    if request.method=='GET':
        return render(request, template)
    # request.method=='POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if not user: # authenticate fail
        return render(request, template, {'error':'登入失敗'})
    if not user.is_active:
        return render(request, template, {'error':'帳號已停用'})
    # login success
    login(request, user)
    messages.success(request, '登入成功')
    return redirect(reverse('main:main'))
        
        
def SignUp(request):
    template = 'account/signup.html'
    if request.method=='GET':
        return render(request, template, {'userForm':UserForm(),'userProfileForm':UserProfileForm()})
    
    # request.method == 'POST':
    userForm = UserForm(request.POST)
    userProfileForm = UserProfileForm(request.POST)
    if not (userForm.is_valid() and userProfileForm.is_valid()):
        return render(request, template, {'userForm':userForm,'userProfileForm':userProfileForm})
    
    user = userForm.save()
    user.set_password(user.password)
    user.save()
    userProfile = userProfileForm.save(commit=False)
    userProfile.user = user
    userProfile.save()
    messages.success(request, '註冊成功')
    return redirect(reverse('main:main'))

def Logout(request):
    logout(request)
    messages.success(request, '歡迎再度光臨')
    return redirect(reverse('main:main'))