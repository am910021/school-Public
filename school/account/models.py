import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Detail(models.Model):
    user = models.OneToOneField(User)
    fullName=models.CharField(max_length=128)
    type = models.IntegerField(default=0)  #0=normal user, 1=manager, 2=developer, 3=administrator
    license = models.CharField(max_length=128,blank=True)
    expire = models.DateTimeField(blank=True)
    
    def __str__(self):
        return self.user.username+"("+ self.fullName +")"
    
    
    def save(self, *args, **kwargs):
        self.expire = timezone.now()+ datetime.timedelta(hours=1)
        super(Detail, self).save(*args, **kwargs)