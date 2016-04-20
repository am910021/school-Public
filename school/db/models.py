from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
    
    
class Demo(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=32)
    dirName = models.CharField(max_length=32, unique=True)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
     
    
class SchoolData(models.Model):
    name = models.CharField(max_length=128)
    type = models.IntegerField(default=0)
    last = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
class Department(models.Model):
    school = models.ForeignKey(SchoolData)
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.school.name+"--"+self.name

    
class Work(models.Model):
    department = models.ForeignKey(Department)
    name = models.CharField(max_length=128)
    rate = models.FloatField(default=0.0)
    type = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(2)])
    year = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(3)])
    def __str__(self):
        return self.name
    
class Salary(models.Model):
    department = models.ForeignKey(Department)
    rate = models.FloatField(default=0.0)
    type = models.IntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(8)])
    
    