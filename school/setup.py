# -*- coding: utf-8 -*-
import os, sys, django
from pip._vendor.distlib.compat import raw_input
import getpass



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
    from main.models import Setting, Menu, Item, ShinyApp, DBItemGroupName, DBItemGroups
    menuName= ('教學', '研究', '國際化', '產學合作及推廣教育', '學生輔導及就業情形', '其他')
    indexNmae= (
('學生參與競賽獲獎人次', '學生參與展覽表演人次', '學生參與公職考試考取人次', '學生考取專業證照人次', '學生考取外語證照人次', '通過教師升等人數', '通過教師評鑑人數', '聘任業師人數(技術聘)', '系所博士班畢業人數', '系統博士生畢業人數', '大一新生各管道註冊率', '推甄錄取最低級分', '碩博士生註冊率', '建置磨課師課程數量', '學生休學原因分析', '學生退學原因分析', '年度四技各系所日夜間部註冊率', '年度碩士班各系所日夜間部註冊率', '年度博士班系所註冊率', '全校學院系所註冊率'),
 ('學生專書出版人次', '學生專書出版篇數', '學生論文出版人士', '學生論文出版篇數', '學生參與國際研討會人數', '學生參與兩岸研討會人數', '教室審稿期刊發表篇數', '教師會議論文發表篇數', '教師專書發表篇數', '教師參與國際會議發表人次', '教師參與學術計畫件數', '教師參與學術研究計畫金額', '教師參與國際合作計畫件數', '教師參與國際合作計畫金額', '教師參與展覽表演活動人次', '教師參與全國性競賽獲獎人次', '教師參與國際性競賽獲獎人次', '辦理學術研討會場數', '辦理國際學術研討會場數', '辦理兩岸學術研討會場數', '圖書收藏冊數', '單位學生之圖書冊數'),
 ('境外生人數', '雙聯學制學生數(IN/OUT)', '國際交流人數', '學生參與國際遊學團人數', '學生參與國際遊學團團數', '學生參與移地教學團數', '國際教師人數'),
 ('學生參與移地教學人數 學生參與移地教學人數', '外籍學者來訪人次', '教師擔任國外交換教師人數', '擔任訪問學者人數', '全英語授課開課數', '建立跨國學位(雙聯學制)學校數', '教師參與業界實務人次', '教師參與產學計畫件數', '教師參與產學計畫金額', '教師技術移轉件數', '教師技術移轉金額', '產學計畫件數及金額'),
 ('產學聯盟家數', '學生實習人數', '學生參與國內實習人數', '學生參與國外實習人數', '畢業生就業率', '系所追蹤畢業生比例', '提供實習機構家數', '提供實習產學聯盟家數', '學生來源分析', '學生畢業薪資分析', '學生畢業出路分析'),
 ()
)
       
    for i in range(0, len(menuName)):
        menu = Menu.objects.create(name=menuName[i], isActive=False)
        menu.order = menu.id
        menu.save()
        for j in range(0, len(indexNmae[i])):
            item = Item.objects.create(menu=menu,name=indexNmae[i][j],isActive=False,)
            item.order = item.id
            item.save()
    Setting.objects.create(name='dirPath', c1='/srv/shiny-server/apps/')
    Setting.objects.create(name='SchoolAPI', c1='https://ip_address_removed/')       
    print(bcolors.OKBLUE + "\n 基本設定執行成功" + bcolors.ENDC)

def checkDB():   
    from django.utils import timezone
    from account.models import User, Profile
    from db.models import Salary, SchoolData, Studsem_all, Department, Work
    from main.models import Setting, Menu, Item, ShinyApp, DBItemGroupName, DBItemGroups
    
    user = len(User.objects.all())
    profile = len(Profile.objects.all())
    salary = len(Salary.objects.all())
    work = len(Work.objects.all())
    department = len(Department.objects.all())
    schoolData = len(SchoolData.objects.all())
    studsem_all = len(Studsem_all.objects.all())
    setting = len(Setting.objects.all())
    menu  = len(Menu.objects.all())
    item  = len(Item.objects.all())
    shinyapp  = len(ShinyApp.objects.all())
    dbitemgroupname  = len(DBItemGroupName.objects.all())
    dbitemgroups  = len(DBItemGroups.objects.all())
    
    
    if user>0 or profile>0 or salary>0 or work>0 or department>0 or schoolData>0 or studsem_all>0 or setting>0 or menu>0 or item>0 or shinyapp>0 or  dbitemgroupname>0 or dbitemgroups>0:
        do = input("資料庫已經有資料，是否清除衝突資料？ yes/no ")
        while not (do=="yes" or do=="no"):
            do = input("資料庫已經有資料，是否清除衝突資料？ yes/no ")
    else:
        return True
    
        
    if do=="no":
        print(bcolors.FAIL + "\n設定失敗。 \n \n" + bcolors.ENDC)
        return False
    else:
        Profile.objects.all().delete()
        User.objects.all().delete()
        Salary.objects.all().delete()
        Work.objects.all().delete()
        Department.objects.all().delete()
        SchoolData.objects.all().delete()
        Studsem_all.objects.all().delete()
        Setting.objects.all().delete()
        ShinyApp.objects.all().delete()
        Item.objects.all().delete()
        Menu.objects.all().delete()
        DBItemGroups.objects.all().delete()
        DBItemGroupName.objects.all().delete()
        return True
        

def createSuperuser():
    from django.utils import timezone
    from account.models import User, Profile
    print(bcolors.OKBLUE + "\n 建立超級管理員帳號" + bcolors.ENDC)
    try:
        while(True):
            username = raw_input("帳號: ")
            check = len(list(User.objects.filter(username=username)))
            if check==0:
                break
            print(bcolors.FAIL + "帳號已經被註冊 \n" + bcolors.ENDC)
        
        password = ""
        password2 = ""
        while(True):
            password = getpass.getpass("密碼: ")
            password2 = getpass.getpass("密碼（再一次）: ")
            if password==password2:
                break
            else:
                print(bcolors.FAIL + "密碼不一樣,重新輸入 \n"  + bcolors.ENDC)
                
        while(True):
            email = raw_input("電子郵件: ")
            
            if email_valid(email):
                break
            print(bcolors.FAIL + "請輸入正確的電子郵件"  + bcolors.ENDC)
        
        admin = User()
        admin.username = username
        admin.set_password(password)
        admin.email = email
        admin.is_superuser = True
        admin.is_staff = True
        admin.is_active = True
        admin.date_joined = timezone.now()
        admin.save()
        
        userProflie = Profile()
        userProflie.user = admin
        userProflie.fullName=username
        userProflie.type = 2  #0=normal user, 1=manager, 2=administrator
        userProflie.isActive = True
        userProflie.save()
        
        print(bcolors.OKBLUE + "\n "+ username +"超級管理員帳號建立成功 \n \n" + bcolors.ENDC)
    except Exception as e:
        s = str(e)
        print(bcolors.FAIL + "\n\n取消建立帳號 \n"  + bcolors.ENDC)
        if """does not exist""" in s:
            print(bcolors.FAIL + "資料庫有問題，請檢查 \n"  + bcolors.ENDC)
  
def email_valid(email):
    from django.core.validators import validate_email
    from django import forms
    try:
        validate_email(email)
        return True
    except forms.ValidationError as e:
        return False

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
    setupDB()
    print(bcolors.OKBLUE + "\n 啟動基本設定" + bcolors.ENDC)
    django.setup()
    if checkDB():
        setup()
        print("\n")
        createSuperuser()

