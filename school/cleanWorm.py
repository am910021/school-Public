# -*- coding: utf-8 -*-
import os

def delData():
    import django
    django.setup()
    from db.models import SchoolData, Department, Work, Salary
    try:
        for i in SchoolData.objects.all():
            for j in Department.objects.filter(school=i):
                Work.objects.filter(department=j).delete() 
                Salary.objects.filter(department=j).delete()
                j.delete()
            print(i.name+"--已清除。")
            i.delete()
        return True
    except:
        return False
                

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
    delData()
    

    
    
    
    
    
    
    
                    
                    
                    
                    
                    
                    
                    