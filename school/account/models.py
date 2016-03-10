from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User)
    fullName=models.CharField(max_length=128)
    type = models.IntegerField(default=0)  #0=normal user, 1=manager, 2=administrator