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
    def __str__(self):
        return self.name

class Item(models.Model):
    menu = models.ForeignKey(Menu)
    name = models.CharField(max_length=128,unique=True)
    permission = models.IntegerField(default=0)
    isActive = models.BooleanField(default=False)
    appQty = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    
    
    
    #def save(self, *args, **kwargs):
    #    self.menu = Menu.objects.get(id=self.menu)
    #    super(Item, self).save(*args, **kwargs)

    
class ShinyApp(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    name = models.CharField(max_length=32)
    dirName = models.CharField(max_length=32, unique=True)
    date = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(ShinyApp, self).save(*args, **kwargs)
        self.item.isActive = True
        self.item.appQty=len(ShinyApp.objects.filter(item=self.item))
        self.item.save()
        
    def delete(self, *args, **kwargs):
        if len(ShinyApp.objects.filter(item=self.item))<=1:
            self.item.isActive = False
            self.item.save()
        super(ShinyApp, self).delete(*args, **kwargs)
        
        
    
    