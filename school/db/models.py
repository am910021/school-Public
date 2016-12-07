from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
    
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
    money = models.IntegerField(default=20000,validators=[MaxValueValidator(80000),MinValueValidator(20000)])
    title = models.CharField(max_length=32)
    type = models.IntegerField(default=0)
    
    
    
class Studsem_all(models.Model):
    sts_acy = models.IntegerField()
    sts_sem = models.IntegerField()
    std_serno = models.CharField(max_length=64)
    cls_id = models.CharField(max_length=16)
    cls_name = models.CharField(max_length=20)
    sec_name = models.CharField(max_length=10)
    sub_name = models.CharField(max_length=10)
    sub_name2 = models.CharField(max_length=10)
    col_fname = models.CharField(max_length=16)
    dep_no = models.CharField(max_length=6)
    dep_fname = models.CharField(max_length=16)
    cls_year = models.IntegerField()
    cls_class = models.CharField(max_length=1)
    sts_status = models.IntegerField()
    
    msg_name = models.CharField(max_length=32)
    sts_ptpone = models.CharField(max_length=1)
    sts_back = models.CharField(max_length=1)
    sts_tsch = models.CharField(max_length=1)
    sts_tdep = models.CharField(max_length=1)
    sts_five = models.CharField(max_length=1)
    std_sex = models.CharField(max_length=1)
    esc_code = models.CharField(max_length=16,blank=True)
    esc_name = models.CharField(max_length=16,blank=True)
    eqa_code = models.CharField(max_length=8)
    eqa_name = models.CharField(max_length=16)
    eid_code = models.CharField(max_length=8)
    eid_name = models.CharField(max_length=24)
    eid_code_a = models.CharField(max_length=8)
    eid_name2 = models.CharField(max_length=24)
    sch_code = models.CharField(max_length=16)
    sch_fname = models.CharField(max_length=32)
    
    sdp_code = models.CharField(max_length=32,blank=True)
    sdp_name = models.CharField(max_length=32,blank=True)
    prv_code_n = models.CharField(max_length=16,blank=True)
    prv_name = models.CharField(max_length=16,blank=True)
    abg_code = models.CharField(max_length=32,blank=True)
    abg_name = models.CharField(max_length=32,blank=True)
    zip_name1 = models.CharField(max_length=16)
    zip_name2 = models.CharField(max_length=16)
    std_entym = models.CharField(max_length=16)
    hst_type = models.CharField(max_length=16,blank=True)
    hst_acy = models.CharField(max_length=16,blank=True)
    hst_sem = models.CharField(max_length=16,blank=True)
    
    
class Studsem(models.Model):
    sts_acy = models.IntegerField()
    sts_sem = models.IntegerField()
    std_serno = models.CharField(max_length=20)
    cls_id = models.CharField(max_length=20)
    sts_status = models.IntegerField()
    sts_reason = models.CharField(blank=True,max_length=5)
    sts_ptpone = models.BooleanField()
    sts_back = models.BooleanField()
    sts_tsch = models.BooleanField()
    sts_tdep = models.BooleanField()
    sts_five = models.BooleanField()
    
class Dep(models.Model):
    acy = models.IntegerField()
    dep_no = models.CharField(max_length=20)
    col_no = models.CharField(max_length=20)
    dep_sname = models.CharField(max_length=32)
    dep_fname = models.CharField(max_length=64)

class Case(models.Model):
    acy = models.IntegerField()
    dep_no = models.CharField(max_length=20)
    cas_key = models.CharField(max_length=20)
    pef_key = models.CharField(max_length=20)
    pep_key = models.CharField(max_length=20)
    cas_no = models.CharField(max_length=64)

    
class Pefund(models.Model):
    pef_key = models.CharField(max_length=10)
    pef_name = models.CharField(max_length=128)
    
class Peplan(models.Model):
    pep_key = models.CharField(max_length=10)
    pep_name = models.CharField(max_length=128)
    
class Pefund_rel(models.Model):
    pef_key = models.CharField(max_length=10)
    pep_key = models.CharField(max_length=10)
    dep_no = models.CharField(max_length=20)
    
    