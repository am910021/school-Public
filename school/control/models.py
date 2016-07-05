from django.db import models
from django.contrib.auth.models import User
from account.models import Profile
from main.models import Menu,Item, DBItemGroupName, DBItemGroups
from .forms import UserForm, UserProfileForm

# Create your models here.
class ItemGroupManage:
    def __init__(self,kwargs):
        self.data = kwargs
    
    def setList(self):
        data = self.data
        data['menu_all'] = Menu.objects.all().iterator()
        #data['user_all'] = User.objects.all().iterator()
        data['user_all'] = Profile.objects.filter(type=0).iterator()
        return
    
    def setEditList(self):
        data = self.data
        try:
            users = []
            items = []
            self.group = DBItemGroupName.objects.get(id=data['id'])
            for i in DBItemGroups.objects.filter(group=self.group).values_list('user', flat=True).distinct():
                users.append(User.objects.get(id=i))
            for i in DBItemGroups.objects.filter(group=self.group).values_list('item', flat=True).distinct():
                items.append(Item.objects.get(id=i))
            data['users'] = users
            data['items'] = items
            data['name'] = self.group.name
            return True
        except Exception as e:
            return False
        
    def save(self,name): 
        data = self.data
        group = self.group
        if(group.name!=name) and (len(DBItemGroupName.objects.filter(name=name))!=0):
            data['name_error'] = "此名稱已經存在，請在試一次．"
            data['name'] = name
            return False
        group.name = name
        group.itemQty=len(self.itemArr)
        group.userQty=len(self.userArr)
        group.save()
        
        DBItemGroups.objects.filter(group=group).delete()
        for i in self.userArr:
            for j in self.itemArr:
                DBItemGroups.objects.create(item=j, user=i, group=group)
        return True
        
    def create(self, name):
        data = self.data
        if(name==""):
            data['name_error'] = "名稱不能留空．"
            return False
        if(len(DBItemGroupName.objects.filter(name=name))>0):
            data['name_error'] = "此名稱已經存在，請在試一次．"
            data['name'] = name
            data['items'] = self.itemArr
            data['users'] = self.userArr
            return False
        
        group = DBItemGroupName.objects.create(name=name, itemQty=len(self.itemArr), userQty=len(self.userArr))
        for i in self.userArr:
            for j in self.itemArr:
                DBItemGroups.objects.create(item=j, user=i, group=group)
        return True
    
    def userValid(self, users):
        data = self.data
        self.userArr = []
        for i in users:
            user = User.objects.filter(id=i)
            print(i)
            if len(user)==1:
                self.userArr.append(user[0])
            else:
                data['user_error'] = "表單資料不合法．"
                self.userArr = []
                return False
        return True
    
    def itemValid(self, items):
        data = self.data
        self.itemArr = []
        for i in items:
            item = Item.objects.filter(id=i)
            if len(item)==1:
                self.itemArr.append(item[0])
            else:
                data['item_error'] = "表單資料不合法．"
                self.itemArr = []
                return False
        return True
    
class AccountManage:
    def __init__(self, kwargs):
        self.data = kwargs
        
    def getUser(self):
        data = self.data
        #users = []
        #for i in DBItemGroups.objects.filter(group=group).values_list('user', flat=True).distinct():
        #    users.append(User.objects.get(id=i)
        data['users'] = User.objects.all()
        
    def getForms(self, instance=None):
        if instance:
            self.data['userForm'] = UserForm(instance=instance)
            self.data['userProfileForm'] = UserProfileForm(instance=instance)
        else:
            self.data['userForm'] = UserForm()
            self.data['userProfileForm'] = UserProfileForm()
        
        
    def getUserDetail(self):
        print(self.data['id'])
        try:
            user = User.objects.get(id=self.data['id'])
            self.data['account'] = user
            self.data['permissions'] = DBItemGroups.objects.filter(user=user).order_by('item').order_by('group')
        except Exception as e: 
            print(e)
            return False
        return True

 