import os
import json
import csv
import urllib.request
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import Setting


def tempResponse(request, *args, **kwargs):
    print(len(args))
    print(kwargs)
    return HttpResponse(404)

def teplateCSV(request):
    s=SchoolApi()
    data = s.getData()
    
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
def CSVapi(request,*args, **kwargs):
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
        if self.isActive:
            return self.getSchoolApi(year, semester)
        return self.getSchoolTemp()
    
    def getSchoolApi(self,year,semester):
        with urllib.request.urlopen(self.url+year+'/'+semester) as response:
            data = json.load(response.read())
            return data
        return None
    
    def getSchoolTemp(self):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'example2.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
        return None
    