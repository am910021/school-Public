# -*- coding: utf-8 -*-
import os
import sys
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

def setup():
    import django
    django.setup()
    from main.models import Menu, Item, ShinyApp
    item = Item.objects.all()
    for i in item:
        app = ShinyApp.objects.filter(item=i)
        if len(app)==0:
            i.isActive=False
        i.appQty = len(ShinyApp.objects.filter(item=i))
        i.save()
    

    print(bcolors.OKBLUE + "\n 設定成功。 \n \n" + bcolors.ENDC)



if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
    print(bcolors.OKBLUE + "\n 啟動基本設定" + bcolors.ENDC)
    #try:
    setup()
    #except Exception as e:
    #    print(bcolors.FAIL + str(e) + bcolors.ENDC)
    
    
    
    
    
    
