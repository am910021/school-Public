import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
import json, requests, django
django.setup()
from db.models import Studsem_all
from main.models import Setting

class SchoolApi:
    def __init__(self):
        print('School Api initialization.')
        self.isActive = False
        self.url=""
        self.csv=""
        try:
            config = Setting.objects.get(name="SchoolAPI")
            if config.c1!="" and config.isActive:
                self.isActive = config.isActive
                self.url = config.c1
        except Exception as e:
            print(e)
        
    def getData(self,name, year=None,semester=None):
        year = ("%03d" %year) if year!=None else None
        semester = str(semester) if semester!=None else None
        if self.isActive:
            return self.getSchoolApi(name, year, semester)
        return self.getSchoolTemp()
    
    def getSchoolApi(self,name, year=None,semester=None):
        try:
            if year==None:
                response = self.getRequest(self.url+name+"/")
            elif semester==None:
                response = self.getRequest(self.url+name+"/"+year+"/")
            else:
                response = self.getRequest(self.url+name+"/"+year+"/"+semester+"/")

            data = json.loads(response)
            return data
        except Exception as e:
            print(e)
            return []
        
    def getApi2(self,name,year,key1,key2):
        year = ("%03d" %year)
        key1 = str(key1)
        key2 = str(key2)
        if self.isActive:
            try:
                response = self.getRequest(self.url+name+"/"+year+"/"+key1+"/"+key2+"/")
                data = json.loads(response)
                return data
            except Exception as e:
                print(e)
                return []
        return self.getSchoolTemp()
    

    def getRequest(self,url):
        isProxy = True
        if isProxy:
            proxies={"https":"http://ip_address_removed:3128"}
            #print(url)
            #print(requests.get(url, proxies=proxies).status_code)
            return requests.get(url, proxies=proxies).text
        else:
            return requests.get(url).text
        
if __name__ == '__main__':
    print("asd")
    s = SchoolApi()
    #https://ip_address_removed/studsem_all/xt%A6/
    #data = s.getData("studsem_all", 101, 1)
    #studsem = Studsem_all
    
    for i in range(84,105): #105
        for j in range(1,3): #1,3
            print("%d--%d" % (i,j))
            for k in s.getData("studsem_all", i, j):
                Studsem_all.objects.get_or_create(
                sts_acy=int(k['sts_acy']),
                sts_sem=int(k['sts_sem']),
                std_serno=k['std_serno'],
                cls_id=k['cls_id'],
                cls_name=k['cls_name'],
                sec_name=k['sec_name'],
                sub_name=k['sub_name'],
                sub_name2=k['sub_name2'],
                col_fname=k['col_fname'],
                dep_no=k['dep_no'],
                dep_fname=k['dep_fname'],
                cls_year=int(k['cls_year']),
                cls_class=k['cls_class'],
                sts_status=int(k['sts_status']),
                msg_name=k['msg_name'],
                sts_ptpone=k['sts_ptpone'],
                sts_back=k['sts_back'],
                sts_tsch=k['sts_tsch'],
                sts_tdep=k['sts_tdep'],
                sts_five=k['sts_five'],
                std_sex=k['std_sex'],
                esc_code=k['esc_code'],
                esc_name=k['esc_name'],
                eqa_code=k['eqa_code'],
                eqa_name=k['eqa_name'],
                eid_code=k['eid_code'],
                eid_name=k['eid_name'],
                eid_code_a=k['eid_code_a'],
                eid_name2=k['eid_name2'],
                sch_code=k['sch_code'],
                sch_fname=k['sch_fname'],
                sdp_code=k['sdp_code'],
                sdp_name=k['sdp_name'],
                prv_code_n=k['prv_code_n'],
                prv_name=k['prv_name'],
                abg_code=k['abg_code'],
                abg_name=k['abg_name'],
                zip_name1=k['zip_name1'],
                zip_name2=k['zip_name2'],
                std_entym=k['std_entym'],
                hst_type=k['hst_type'],
                hst_acy=k['hst_acy'],
                hst_sem=k['hst_sem'],)
    
            
            