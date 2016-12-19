import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
import json, requests, django
django.setup()
from db.models import Studsem_all, Studsem, Pefund, Peplan, Pefund_rel, Case
from main.models import Setting

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
        
def studsem_all_update():
    s = SchoolApi()
    for i in range(100,106): #84-105 
        for j in range(1,3): #1,3
            Studsem_all.objects.filter(sts_acy=i, sts_sem=j).delete()
            url = "https://ip_address_removed/studsem_all/%03d/%d/" % (i, j)
            data = json.loads(s.getRequest(url))
            print(url)
            for k in data:
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
            print("studsem_all %d學年度 第%d學期 己更新" % (i,j))
    print("studsem_all 己更新")
        
def studsem_update():
    s = SchoolApi()
    for i in range(98,106): #資料從84年開始
        for j in range(1,3): # 1 2，1 2，1 2
            Studsem.objects.filter(sts_acy=i, sts_sem=j).delete()
            url = "https://ip_address_removed/studsem/%03d/%d/" % (i, j)
            data = json.loads(s.getRequest(url))
            for d in data:
                Studsem.objects.create(
                                    sts_acy = int(d['sts_acy']),
                                    sts_sem = int(d['sts_sem']),
                                    std_serno = d['std_serno'],
                                    cls_id = d['cls_id'],
                                    sts_status = int(d['sts_status']),
                                    sts_reason = d['sts_reason'],
                                    sts_ptpone = True if d['sts_ptpone']=="Y" else False,
                                    sts_back = True if d['sts_back']=="Y" else False,
                                    sts_tsch = True if d['sts_tsch']=="Y" else False,
                                    sts_tdep = True if d['sts_tdep']=="Y" else False,
                                    sts_five = True if d['sts_five']=="Y" else False
                                    )
            print("studsem %d學年度 第%d學期 己更新" % (i,j))
    print("studsem 己更新")
        
def case_update():
    s = SchoolApi()
    
    print("pefund 開始更新")
    Pefund.objects.all().delete()
    url = "https://ip_address_removed/pefund/"
    data = json.loads(s.getRequest(url))
    for d in data:
        Pefund.objects.create(pef_key = d['pef_key'],
                              pef_name = d['pef_name']
                              )
    print("pefund 更新完成")
    ##
    print("peplan 開始更新")
    Peplan.objects.all().delete()
    url = "https://ip_address_removed/peplan/"
    data = json.loads(s.getRequest(url))
    for d in data:
        Peplan.objects.create(pep_key = d['pep_key'],
                              pep_name = d['pep_name']
                              )
    print("peplan 更新完成")       
    ##
    print("pefund_rel 開始更新")
    Pefund_rel.objects.all().delete()
    url = "https://ip_address_removed/pefund_rel/"
    data = json.loads(s.getRequest(url))
    for d in data:
        Pefund_rel.objects.create(
                                  pef_key = d['pef_key'],
                                  pep_key = d['pep_key'],
                                  dep_no = d['dep_no']
                              )
    print("pefund_rel 更新完成")   
    ## 
    print("Case 開始更新")
    Case.objects.all().delete()
    pefund_rel = Pefund_rel.objects.all()
    for i in range(84,106):
        for j in pefund_rel:
            url = "https://ip_address_removed/case/%03d/%s/%s/" % (i, j.pef_key, j.pep_key)
            print(url)
            data = json.loads(s.getRequest(url))
            for d in data:
                Case.objects.create(acy = int(d['acy']),
                                    dep_no = d['dep_no'],
                                    cas_key = d['cas_key'],
                                    pef_key = d['pef_key'],
                                    pep_key = d['pep_key'],
                                    cas_no = d['cas_no'],
                                    )
        print("Case %d 學年度己更新"% (i))
    print("Case 更新完成")   
        
if __name__ == '__main__':
    #studsem_all_update()
    studsem_update()
    #case_update()
    
            
            
