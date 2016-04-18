import os, shutil
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Setting(models.Model):
    name = models.CharField(max_length=15, unique=True, blank=False)
    isActive = models.BooleanField(default=False)
    c1 = models.CharField(max_length=128, blank=True)
    c2 = models.CharField(max_length=128, blank=True)
    c3 = models.CharField(max_length=128, blank=True)
    c4 = models.CharField(max_length=128, blank=True)
    c5 = models.CharField(max_length=128, blank=True)
    c6 = models.CharField(max_length=128, blank=True)
    c7 = models.CharField(max_length=128, blank=True)
    c8 = models.CharField(max_length=128, blank=True)
    time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Menu(models.Model):
    name = models.CharField(max_length=128,unique=True)
    permission = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True)
    itemQty = models.IntegerField(default=0)
    itemActiveQty = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        item = Item.objects.filter(menu=self)
        self.itemQty = len(item)
        self.itemActiveQty = len(item.filter(isActive=True))
        super(Menu, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        for i in Item.objects.filter(menu=self):
            i.delete()
        super(Menu, self).delete(*args, **kwargs)

class Item(models.Model):
    menu = models.ForeignKey(Menu)
    name = models.CharField(max_length=128,unique=True)
    permission = models.IntegerField(default=0)
    isActive = models.BooleanField(default=False)
    appQty = models.IntegerField(default=0)
    activeQty = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)
        if self.appQty>0:
            self.menu.isActive = True
        elif self.appQty==0:
            self.menu.isActive = False
        self.menu.save()

    def delete(self, *args, **kwargs):
        for i in ShinyApp.objects.filter(item=self):
            i.delete()
            
        menu = self.menu
        super(Item, self).delete(*args, **kwargs)
        l = len(Item.objects.filter(menu=menu, isActive=True))
        if l==0:
            menu.isActive = False
        menu.appQty=l
        menu.save()

    
class ShinyApp(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    name = models.CharField(max_length=64)
    fileName = models.CharField(max_length=64, blank=True)
    fileType = models.CharField(max_length=64, blank=True)
    dirName = models.CharField(max_length=64, unique=True)
    date = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(ShinyApp, self).save(*args, **kwargs)
        item = ShinyApp.objects.filter(item=self.item)
        self.item.isActive = True
        self.item.appQty=len(item)
        self.item.save()
        
    def delete(self, *args, **kwargs):
        try:
            config = Setting.objects.get(name="dirPath")
            shutil.rmtree(config.c1+self.dirName)
        except Exception as e:
            print(e)
        super(ShinyApp, self).delete(*args, **kwargs)
        l = len(ShinyApp.objects.filter(item=self.item))
        if l==0:
            self.item.isActive = False
        self.item.appQty=l
        self.item.save()
        
        
        
        
    
    