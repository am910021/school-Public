from django.db import models
from django.contrib.auth.models import User
from account.models import Profile
from main.models import Menu,Item, DBGroupName, DBGroupItem, DBGroupUser
from .forms import UserForm, UserProfileForm

# Create your models here.
class ItemGroupManage:
    def __init__(self,kwargs):
        self.data = kwargs
    
    def setList(self):
        data = self.data
        user = []
        data['menu_all'] = Menu.objects.all().iterator()
        data['user_all'] = Profile.objects.filter(type=0, level=0).iterator()
        
        return
    
    def setEditList(self):
        data = self.data
        try:
            users = []
            items = []
            self.group = DBGroupName.objects.get(id=data['id'])
            level = self.group.level
            if level==0:
                for i in DBGroupUser.objects.filter(group=self.group):
                    users.append(i.user)
            for i in DBGroupItem.objects.filter(group=self.group).values_list('item', flat=True).distinct():
                items.append(Item.objects.get(id=i))
            data['users'] = users
            data['items'] = items
            data['name'] = self.group.name
            data['level'] = level
            return True
        except Exception as e:
            print(e)
            return False
        
    def save(self,name): 
        data = self.data
        group = self.group
        if(group.name!=name) and (len(DBGroupName.objects.filter(name=name))!=0):
            data['name_error'] = "此名稱已經存在，請在試一次．"
            data['name'] = name
            return False
        group.name = name
        group.itemQty=len(self.itemArr)
        group.userQty=len(self.userArr)
        group.save()
        
        if group.level==0:
            DBGroupUser.objects.filter(group=group).delete()
            for i in self.userArr:
                DBGroupUser.objects.create(user=i, group=group)
            
        DBGroupItem.objects.filter(group=group).delete()
        for j in self.itemArr:
            DBGroupItem.objects.create(item=j, group=group)     
        return True
        
    def create(self, name):
        data = self.data
        if(name==""):
            data['name_error'] = "名稱不能留空．"
            return False
        if(len(DBGroupName.objects.filter(name=name))>0):
            data['name_error'] = "此名稱已經存在，請在試一次．"
            data['name'] = name
            data['items'] = self.itemArr
            data['users'] = self.userArr
            return False
        group = DBGroupName.objects.create(name=name, itemQty=len(self.itemArr), userQty=len(self.userArr))
        for i in self.userArr:
            DBGroupUser.objects.create(user=i, group=group)
        for j in self.itemArr:
            DBGroupItem.objects.create(item=j, group=group)     
        return True
    
    def userValid(self, users):
        data = self.data
        self.userArr = []
        for i in users:
            user = User.objects.filter(id=i)
            if len(user)==1:
                self.userArr.append(user[0])
            else:
                data['user_error'] = "表單資料不合法．"
                self.userArr = []
                print("user fail")
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
                print("item fail")
                return False
        return True
    
    def getDetail(self):
        data = self.data
        try:
            users = []
            items = []
            group = DBGroupName.objects.get(id=data['id'])
            if group.level==0:
                for i in DBGroupUser.objects.filter(group=group):
                    users.append(i.user)
            for i in DBGroupItem.objects.filter(group=group).values_list('item', flat=True).distinct():
                items.append(Item.objects.get(id=i))
            data['users'] = users
            data['items'] = items
            data['group'] = group
            return True
        except Exception as e:
            print(e)
            return False
    
class AccountManage:
    def __init__(self, kwargs):
        self.data = kwargs
        
    def getUser(self):
        data = self.data
        #users = []
        #for i in DBGroupItem.objects.filter(group=group).values_list('user', flat=True).distinct():
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
            item = []
            user = User.objects.get(id=self.data['id'])
            self.data['account'] = user
            profile = user.profile
            if profile.adAdmin or profile.adAdmin2 or profile.atAdmin or profile.atAdmin2:
                for i in DBGroupItem.objects.filter(group=profile.adAdmin):
                    item.append(i)
                for i in DBGroupItem.objects.filter(group=profile.adAdmin2):
                    item.append(i)
                for i in DBGroupItem.objects.filter(group=profile.atAdmin):
                    item.append(i)
                for i in DBGroupItem.objects.filter(group=profile.atAdmin2):
                    item.append(i)
            else:
                for i in DBGroupUser.objects.filter(user=user):
                    for j in DBGroupItem.objects.filter(group=i.group):
                        item.append(j)
            self.data['permissions'] = item
        except Exception as e: 
            print(e)
            return False
        return True

 