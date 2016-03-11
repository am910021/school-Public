import os
import json
import csv
import urllib.request
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import Setting


def tempResponse(request, *args, **kwargs):
    print(len(args))
    print(kwargs)
    return HttpResponse(404)

def teplateCSV(request):
    s=SchoolApi()
    data = s.getSchoolTemp()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    
    writer = csv.writer(response)
    heads=[]
    for i in data[0].keys():
        heads.append(i)
    writer.writerow(heads)
    for i in data:
        print()
        writer.writerow(list(i.values()))
    
    return response


class SchoolApi:
    def __init__(self):
        print('SchoolApi initialization.')
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
        file_path = os.path.join(module_dir, 'example.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
        return None
 
    def dumpCSV(self,data):
        response = HttpResponse(content_type='text/csv')
        writer = csv.writer(response)
        heads=[]
        for i in data[0].keys():
            heads.append(i)
        
        writer.writerow(heads)
        
        for i in data:
            print()
            writer.writerow(list(i.values()))
    
        return response
    
    