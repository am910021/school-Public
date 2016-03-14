import os
import json
import csv
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from account.models import Detail
from main.models import Setting
from _ast import Str

def schoolAPI(request, *args, **kwargs):
    try:
        user = Detail.objects.filter(license=kwargs['license'])
        if not user:
            return HttpResponse("login fail",content_type='text/plain')
    except Exception as e:
        print(e)
        return HttpResponse("login fail",content_type='text/plain')
    
    
    year = kwargs['year']
    semester = kwargs['semester']
    s = SchoolApi()
    data = s.getData(year, semester)
    
    if data==None:
        return HttpResponse("None Data",content_type='text/plain')
    
    heads=[]
    for i in data[0].keys():
        heads.append(i)  
    s=','.join(heads)  
    for i in data:
        s+="\n"
        s+=','.join(i.values())
    return HttpResponse(s,content_type='text/plain')

def schoolAPI2(request, *args, **kwargs):
    try:
        user = Detail.objects.filter(license=kwargs['license'])
        if not user:
            return HttpResponse("login fail",content_type='text/plain')
    except Exception as e:
        print(e)
        return HttpResponse("login fail",content_type='text/plain')
    
    if 'startYear' not in kwargs or 'endYear' not in kwargs or 'semester' not in kwargs:
        return HttpResponse("input fail",content_type='text/plain')
    
    startYear = int(kwargs['startYear'])
    endYear = int(kwargs['endYear'])
    semester = int(kwargs['semester'])
    
    data = []
    s = SchoolApi()
    for i in range(startYear,endYear+1):
        if semester>0:
            print(len(s.getData(i, semester)))
            data += s.getData(i, semester)
        else:
            data += s.getData(i, 1)
            data += s.getData(i, 2)
    
    if len(data)==0:
        return HttpResponse("None Data",content_type='text/plain')
    
    heads=[]
    for i in data[0].keys():
        heads.append(i)  
    s=','.join(heads)  
    for i in data:
        s+="\n"
        s+=','.join(i.values())
    return HttpResponse(s,content_type='text/plain')

def templateJSON(request, *args, **kwargs):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'example.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
            return JsonResponse(data,safe=False)        



def CSVapi(request,*args, **kwargs):
    year = kwargs['year']
    semester = kwargs['semester']
    s = SchoolApi()
    data = s.getData(year, semester)
    
    heads=[]
    for i in data[0].keys():
        heads.append(i)  
    s=','.join(heads)  
    for i in data:
        s+="\n"
        s+=','.join(i.values())
    return HttpResponse(s,content_type='text/plain')


def CSVapi_temp(request,*args, **kwargs):
    year = kwargs['year']
    semester = kwargs['semester']
    s = SchoolApi()
    data = s.getData(year, semester)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)
    heads=[]
    for i in data[0].keys():
        heads.append(i)
    writer.writerow(heads)
    for i in data:
        writer.writerow(list(i.values()))

    return response
   
@login_required
def CSVapi2(request, *args, **kwargs):
    year = kwargs['year']
    semester = kwargs['semester']
    category = Category()
    data = []
    if kwargs['category'].isdigit():
        data += category.Mode(year, semester,int(kwargs['category']))
    else:
        if len(kwargs['category'].split("-"))==2:
            data += category.Mode2(year, semester,sorted(kwargs['category'].split("-"),reverse=True))
        else:
            data += category.Mode2(year, semester,sorted(kwargs['category'].split("-"),reverse=True))
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)
    heads=[]
    for i in data[0].keys():
        heads.append(i)
    writer.writerow(heads)
    for i in data:
        writer.writerow(list(i.values()))
    return response

class Category:
    def __init__(self):
        print('Classification process initialization.')
        
    def Mode(self,year, semester,category):
        data = []
        if category==0:
            return data
        # 等資料庫
        #if category>=1:
        return data

    def Mode2(self,year, semester,category):
        data = []
        for i in category:
            if i==0:
                return data
            # 等資料庫
        return data

    def Mode3(self,year, semester,category):
        data = []
        for i in category:
            if i==0:
                return data
            # 等資料庫
        return data

class SchoolApi:
    def __init__(self):
        print('School Api initialization.')
        self.isActive = False
        self.url=""
        try:
            config = Setting.objects.get(name="SchoolAPI")
            if config.c1!="" and config.isActive:
                self.isActive = config.isActive
                self.url = config.c1
        except Exception as e:
            print(e)
        
    def getData(self,year,semester):
        year = str(year)
        semester = str(semester)
        if self.isActive:
            return self.getSchoolApi(year, semester)
        return self.getSchoolTemp()
    
    def getSchoolApi(self,year,semester):
        try:
            response = urlopen(self.url+year+semester+"/"+semester+"/")
            data = json.loads(response.read().decode('utf8'))
            response.close()
            return data
        except Exception as e:
            print(e)
            return []


    def getSchoolTemp(self):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'example.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
        return []
    