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
    
class Student(models.Model):
    sts_acy = models.CharField(max_length=32)
    sts_sem = models.CharField(max_length=32)
    std_serno = models.CharField(max_length=32)
    cls_id = models.CharField(max_length=32)
    sts_status = models.CharField(max_length=32)
    sts_reason = models.CharField(max_length=32)
    sts_ptpone = models.CharField(max_length=32)
    sts_back = models.CharField(max_length=32)
    sts_tsch = models.CharField(max_length=32)
    sts_tdep = models.CharField(max_length=32)
    sts_five = models.CharField(max_length=32)