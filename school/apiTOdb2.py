import os, csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
import django
django.setup()
from db.models import Studsem, Dep
from main.models import Setting
        
if __name__ == '__main__':
    Studsem.objects.all().delete()
    
    
    # studsem
    print("Studsem 更新啟動。")
    for i in range(101,105):
        for j in range(1,3):
            file = "/home/yuri/IRDATA/studsem/studsem%d_%d.csv" % (i,j)
            with open(file, encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:  
                    Studsem.objects.create(
                                           sts_acy = int(row['sts_acy']),
                                           sts_sem = int(row['sts_sem']),
                                           std_serno = row['std_serno'],
                                           cls_id = row['cls_id'],
                                           sts_status = int(row['sts_status']),
                                           sts_reason = row['sts_reason'],
                                            
                                           sts_ptpone = True if row['sts_ptpone']=="Y" else False,
                                           sts_back = True if row['sts_back']=="Y" else False,
                                           sts_tsch = True if row['sts_tsch']=="Y" else False,
                                           sts_tdep = True if row['sts_tdep']=="Y" else False,
                                           sts_five = True if row['sts_five']=="Y" else False
                                           )
    print("Studsem 更新完成。")
                 

    # dep
    print("Dep2 更新啟動。")
    Dep.objects.all().delete()
    file = "/home/yuri/IRDATA/dep/dep.csv"
    with open(file, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:  
            Dep.objects.create(
                               acy = int(row['acy']),
                               dep_no = row['dep_no'],
                               col_no = row['col_no'],
                               dep_sname = row['dep_sname'],
                               dep_fname = row['dep_fname']
                               )
    print("Dep2 更新完成。")
            