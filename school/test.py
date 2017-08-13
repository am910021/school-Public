import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
import json, requests, django
django.setup()
from db.models import Case, Case_funds
from main.models import Setting
from time import sleep

class SchoolApi: 
    def getRequest(self,url):
        isProxy = False
        if isProxy:
            proxies={"https":"http://ip_address_removed:3128"}
            #print(url)
            #print(requests.get(url, proxies=proxies).status_code)
            return requests.get(url, proxies=proxies).text
        else:
            return requests.get(url).text
        


def case2_update():
    s = SchoolApi()
    
    print("case_funds 開始更新")
    
    case = Case.objects.values("cas_key").distinct()
    Case_funds.objects.all().delete()
    url_s = "https://ip_address_removed/case_funds/%s/"
    for c in case:
        url = url_s % (c["cas_key"])
        data = json.loads(s.getRequest(url))
        print(url)
        sleep(0.3)
        d= data[0]
        Case_funds.objects.create(cas_key = d['cas_key'],cas_funds = d['cas_funds'])
    print("case_funds 更新完成")

    
        
        
if __name__ == '__main__':
    case2_update()
    
            
            
