import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
import json, requests, django
django.setup()
from main.models import Setting

def update_system():

    version = ""
    try:
        f = open("version.txt", "r")
        r = f.readline()
        v = r.split("-")[1]
        version = v.replace("\n","")
    except:
        version = "unknow"

    record = Setting.objects.filter(name='SITE_VERSION')
    if len(record) <= 0:
        Setting.objects.get_or_create(name='SITE_VERSION',c1=version)
    else:
        data = record[0]
        data.c1 = version
        data.save()
        
    print("version up to " + version)
        
if __name__ == '__main__':
    update_system()
    