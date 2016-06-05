# -*- coding: utf-8 -*-
import os

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
    for i in ShinyApp.objects.all():
        i.save()

    print(bcolors.OKBLUE + "\n 設定成功。 \n \n" + bcolors.ENDC)



if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
    print(bcolors.OKBLUE + "\n 啟動基本設定" + bcolors.ENDC)
    setup()

    
    
    
    
    
    
