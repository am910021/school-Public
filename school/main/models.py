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
        return "%s (%d)" % (self.name, self.id)
    
class Menu(models.Model):
    name = models.CharField(max_length=128,unique=True)
    permission = models.IntegerField(default=0)
    isActive = models.BooleanField(default=False)
    itemQty = models.IntegerField(default=0)
    activeQty = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    def __str__(self):
        return "%s (%d)" % (self.name, self.id)
        
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
        return "%s (%d)" % (self.name, self.id)

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)
        self.countQty()
        

    def delete(self, *args, **kwargs):
        for i in ShinyApp.objects.filter(item=self):
            i.delete()
        super(Item, self).delete(*args, **kwargs)
        self.countQty()
        
    def countQty(self):
        item = Item.objects.filter(menu=self.menu)
        self.menu.itemQty=len(item)
        self.menu.activeQty = len(item.filter(isActive=True))
        self.menu.isActive = True if self.menu.activeQty > 0 else False
        self.menu.save()

    
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
    time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "%s (%d)" % (self.name, self.id)

    def save(self, *args, **kwargs):
        super(ShinyApp, self).save(*args, **kwargs)
        self.countQty()
        
    def delete(self, *args, **kwargs):
        try:
            config = Setting.objects.get(name="dirPath")
            shutil.rmtree(config.c1+self.dirName)
        except Exception as e:
            print(e)
        super(ShinyApp, self).delete(*args, **kwargs)
        self.countQty()
        
    def countQty(self):
        shiny = ShinyApp.objects.filter(item=self.item)
        self.item.appQty = len(shiny)
        self.item.activeQty = len(shiny.filter(isActive=True))
        self.item.isActive = True if self.item.activeQty>0 else False
        self.item.save()
        
        
    
    