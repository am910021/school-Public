import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from main.models import DBGroupItem, DBGroupName
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User)
    fullName=models.CharField(max_length=128)
    type = models.IntegerField(default=0)  #0=normal user, 1=manager, 2=administrator
    license = models.CharField(max_length=128,blank=True)
    expire = models.DateTimeField(blank=True)
    isActive = models.BooleanField(default=True)
    isAuth = models.BooleanField(default = True)
    group = models.ForeignKey(DBGroupName, blank=True, null=True)
    
    def __str__(self):
        return self.user.username+"("+ self.fullName +")"
    
    
    def save(self, *args, **kwargs):
        self.expire = timezone.now()+ datetime.timedelta(hours=1)
        super(Profile, self).save(*args, **kwargs)

