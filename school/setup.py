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
    
def setupDB():
    sys.argv.append("migrate")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


def setup():
    import django
    django.setup()
    from main.models import Menu, Item, ShinyApp
    menuName= ('教學', '研究', '國際化', '產學合作及推廣教育','學生輔導及就業情形')
    indexNmae= (
                ('學生參與競賽獲獎人次', '學生參與展覽表演人次', '學生參與公職考試考取人次', '學生考取專業證照人次', '學生考取外語證照人次', '通過教師升等人數', '通過教師評鑑人數', '聘任業師人數(技術聘)', '學生二一退學人數', '系所博士班畢業人數', '系統博士生畢業人數', '大一新生各管道註冊率', '推甄錄取最低級分', '碩博士生註冊率', '建置磨課師課程數量'),
                ('學生專書出版人次', '學生專書出版篇數', '學生論文出版人士', '學生論文出版篇數', '學生參與國際研討會人數', '學生參與兩岸研討會人數', '教室審稿期刊發表篇數', '教師會議論文發表篇數', '教師專書發表篇數', '教師參與國際會議發表人次', '教師參與學術計畫件數', '教師參與學術研究計畫金額', '教師參與國際合作計畫件數', '教師參與國際合作計畫金額', '教師參與展覽表演活動人次', '教師參與全國性競賽獲獎人次', '教師參與國際性競賽獲獎人次', '辦理學術研討會場數', '辦理國際學術研討會場數', '辦理兩岸學術研討會場數'),
                ('境外生人數', '雙聯學制學生數(IN/OUT)', '國際交流人數', '學生參與國際遊學團人數', '學生參與國際遊學團團數'),
                ('學生參與移地教學人數 學生參與移地教學人數', '學生參與移地教學團數', '國際教師人數', '外籍學者來訪人次', '教師擔任國外交換教師人數', '擔任訪問學者人數', '全英語授課開課數', '建立跨國學位(雙聯學制)學校數', '教師參與業界實務人次', '教師參與產學計畫件數', '教師參與產學計畫金額', '教師技術移轉件數', '教師技術移轉金額'),
                ('產學聯盟家數', '學生實習人數', '學生參與國內實習人數', '學生參與國外實習人數', '畢業生就業率', '系所追蹤畢業生比例', '提供實習機構家教', '提供實習產學聯盟家數')
                )
    
    menu = Menu.objects.all()
    item = Item.objects.all()
    
    do = ""
    if menu or item:
        do = input("資料庫已經有資料，是否清除衝突資料？ yes/no ")
        while not (do=="yes" or do=="no"):
            do = input("資料庫已經有資料，是否清除衝突資料？ yes/no ")
    
        
    if do=="no":
        print(bcolors.FAIL + "\n設定失敗。 \n \n" + bcolors.ENDC)
        return
    else:
        menu.delete()
        item.delete()
        ShinyApp.objects.all().delete()
        
    for i in range(0, len(menuName)):
        menu = Menu.objects.create(name=menuName[i], permission=0, isActive=False)
        menu.order = menu.id
        menu.save()
        #name
        #permission
        #isActive
        for j in range(0, len(indexNmae[i])):
            item = Item.objects.create(menu=menu,
                                name=indexNmae[i][j],
                                permission=0,
                                isActive=False,
                                )
            item.order = item.id
            item.save()
    print(bcolors.OKBLUE + "\n 設定成功。 \n \n" + bcolors.ENDC)



if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
    setupDB()
    print(bcolors.OKBLUE + "\n 啟動基本設定" + bcolors.ENDC)
    #try:
    setup()
    #except Exception as e:
    #    print(bcolors.FAIL + str(e) + bcolors.ENDC)
    
    
    
    
    
    
