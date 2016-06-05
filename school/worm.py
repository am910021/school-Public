# -*- coding: utf-8 -*-
import os
from pip._vendor.distlib.compat import raw_input
import requests
from bs4 import BeautifulSoup



def getWeb():
    import django
    django.setup()
    from db.models import SchoolData, Department, Work, Salary
    
    res=requests.get("http://www.104.com.tw/jb/career/department/navigation?browser=2%C2%B0ree=3")
    res.encoding='utf8'
    soup = BeautifulSoup(res.text, "html.parser")
    mylist=[]
    for first in soup.select('.a2'):
        d='http://www.104.com.tw'+first['href']
        mylist.append(d)
        """這裡是找學校的網址"""
        
    for sec in mylist:
        res2=requests.get(sec)
        res2.encoding='utf8'
        soup2 = BeautifulSoup(res2.text, "html.parser")
        """ 這裡我只是不太想做太多層for 所以用個list 包網址在跑"""
        
        for thi in soup2.select('.a2'):
            res3=requests.get('http://www.104.com.tw'+thi['href'])
            res3.encoding='utf8'
            soup3 = BeautifulSoup(res3.text, "html.parser")
            """這裡是找學校系所的網址"""
            
            title = soup3.select(".title.cf")[0].select("h1[class~=h1]")[0]
            university = title.select("a")[0].text.replace(" ","")
            department = title.select("a")[1].text.replace(" ","")
            db_school = SchoolData.objects.get_or_create(name=university)[0]
            db_department = Department.objects.get_or_create(name=department, school=db_school)[0]
                
            for fou in soup3.select('.yearContent'):
                year =-1 #記錄年
                for div in fou.select("div[class~=cf]"): #找<div class="cf">
                    year+=1
                    type=-1
                    for dl in div.select("dl[class~=p2]"): #找<dl class="p2">
                        type+=1
                        for dd in dl.select("dd[class~=cf]"): #找<dd class="cf">
                            p = dd.select("span")[0].text.replace(" ","") #記錄百分比 去除中間的空白，在後面加空白
                            p = float(p.replace("%",""))
                            data = (dd.select("a")[0].text if dd.select("a") else "其他")
                            Work.objects.create(department=db_department,name=data,rate=p,type=type,year=year)
                            
            try:
                r=[0,0,0,0]
                title = soup3.select("li.title.row.p1")[0]
                title2 = soup3.select("ul.w-sort.w-sortOption")[0].select("a.a2")
                t1 = title.select("strong")[0].text.split(" ")[1]
                t2 = title2[0].text.replace(" ","-")
                t3 = title2[1].text.replace(" ","-")
                t4 = title2[2].text.replace(" ","-")
                #print("%s  %s  %s  %s" % (t1,t2,t3,t4))
                tData=[t1,t2,t3,t4]
                for fou in soup3.select('.rangeData'):
                    content = fou.select("div.content")
                    #if(len(fou.select("div.main")[0].select("div.content"))==0):
                    #    break;
                    #print(len(list(content)))
                    i= -1 if len(list(content))==4 else 0
                    for dd in content:
                        i+=1
                        webRate = float(dd.select("strong")[0].text)
                        rate=float(round(webRate-r[i],2))
                        r[i]=webRate
                        m = int(dd.select("strong")[1].text.replace(" ",""))
                        Salary.objects.create(department=db_department,title=tData[i],rate=rate,money=m,type=i)         
                print(department+"--加入完成")
            except Exception as e:
                print("錯誤："+str(e))
        print(university+"--加入完成")

def checkDate():
    import django
    django.setup()
    from db.models import SchoolData
    l = len(list(SchoolData.objects.all()))
    if l>0:
        print("資料已存在。")
        while(True):
            res = raw_input("確定更新資料 yes no？ ")
            if res=="yes":
                return True
            elif res=="no":
                return False
            else:
                print("你在開玩笑嗎？ 請選擇 yes 或 no。\r\n")
    return True
    
    
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
    if checkDate() and delData():
        print("資料已全數清除，準備更新． \r\n\r\n")
        getWeb()
    

    
    
    
    
    
    
    
                    
                    
                    
                    
                    
                    
                    