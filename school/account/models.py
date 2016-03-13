from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Detail(models.Model):
    user = models.OneToOneField(User)
    fullName=models.CharField(max_length=128)
    type = models.IntegerField(default=0)  #0=normal user, 1=manager, 2=developer, 3=administrator
    
    def __str__(self):
        return self.user.username+"("+ self.fullName +")"