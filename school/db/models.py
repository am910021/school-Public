from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class School(models.Model):
    year = models.CharField(max_length=4)
    
    
class Demo(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=32)
    dirName = models.CharField(max_length=32, unique=True)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name