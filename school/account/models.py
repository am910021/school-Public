import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from main.models import DBItemGroups, DBItemGroupName
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User)
    fullName=models.CharField(max_length=128)
    type = models.IntegerField(default=0)  #0=normal user, 1=manager, 2=administrator
    license = models.CharField(max_length=128,blank=True)
    expire = models.DateTimeField(blank=True)
    isActive = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username+"("+ self.fullName +")"
    
    
    def save(self, *args, **kwargs):
        self.expire = timezone.now()+ datetime.timedelta(hours=1)
        super(Profile, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        groups = DBItemGroups.objects.filter(user=self.user)
        if len(groups)>0:
            for i in groups.values_list('group', flat=True).distinct():
                group = DBItemGroupName.objects.get(id=i)
                userCount = len(DBItemGroups.objects.filter(group=group).exclude(user=self.user).values_list('user', flat=True).distinct())
                itemCount = len(DBItemGroups.objects.filter(group=group).exclude(user=self.user).values_list('item', flat=True).distinct())
                group.itemQty=itemCount
                group.userQty=userCount
                group.save() 
        groups.delete()
        super(Profile, self).delete(*args, **kwargs)