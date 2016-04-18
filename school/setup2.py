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
    for i in Menu.objects.all():
        for j in Item.objects.filter(menu=i):
            for k in ShinyApp.objects.filter(item=j):
                k.order = k.id
                k.item.appQty=len(list(ShinyApp.objects.filter(item = k.item)))
                if k.item.appQty>0:
                    k.item.isActive = True
                else:
                    k.item.isActive = False
                k.item.save()
                k.save()
            j.order = j.id
        i.order = i.id
        i.save()

    print(bcolors.OKBLUE + "\n 設定成功。 \n \n" + bcolors.ENDC)



if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
    print(bcolors.OKBLUE + "\n 啟動基本設定" + bcolors.ENDC)
    setup()

    
    
    
    
    
    
