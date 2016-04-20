import requests
from bs4 import BeautifulSoup

res=requests.get("http://www.104.com.tw/jb/career/department/navigation?browser=2%C2%B0ree=3")
res.encoding='utf8'
soup = BeautifulSoup(res.text, "html.parser")
mylist=[]
for first in soup.select('.a2'):
    d='http://www.104.com.tw'+first['href']
    mylist.append(d)
    """這裡是找學校的網址"""
    
count = 0
for sec in mylist:
    count+=1
    if count>2:
        break
    res2=requests.get(sec)
    res2.encoding='utf8'
    soup2 = BeautifulSoup(res2.text, "html.parser")
    """ 這裡我只是不太想做太多層for 所以用個list 包網址在跑"""
    
    for thi in soup2.select('.a2'):
        url = 'http://www.104.com.tw'+thi['href']
        res3=requests.get(url)
        res3.encoding='utf8'
        soup3 = BeautifulSoup(res3.text, "html.parser")
        """這裡是找學校系所的網址"""
        
        title = soup3.select(".title.cf")[0].select("h1[class~=h1]")[0]
        university = title.select("a")[0].text.replace(" ","")
        department = title.select("a")[1].text.replace(" ","")
        print(university+"-"+department) #學校名稱
        print(url)
        for fou in soup3.select('.rangeData'):
            for dd in fou.select('.main'):
                if(len(dd.select("strong"))>0):
                    print(dd.select("strong")[0].text)
            print("")       
                    
        