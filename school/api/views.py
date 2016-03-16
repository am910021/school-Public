import os
import json
import threading,time
from urllib.request import urlopen
import requests
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from account.models import Detail
from main.models import Setting
from _ast import Str

def ArgsError(request, *args, **kwargs):
    return HttpResponse("ArgumentsError", content_type='text/plain')


def schoolAPI(request, *args, **kwargs):
    if request.user.username=="" or request.user.detail.type <2:
        try:
            user = Detail.objects.filter(license=kwargs['license'])
            if not user:
                return HttpResponse("LoginFail", content_type='text/plain')
        except Exception as e:
            print(e)
            return HttpResponse("LoginFail", content_type='text/plain')
    
    
    name = kwargs['name']
    year = int(kwargs['year']) if 'year' in kwargs else None
    semester = int(kwargs['semester']) if 'semester' in kwargs else None
    s = SchoolApi()
    data = []
    
    if semester==None:
        data += s.getData(name, year)
    elif semester>0:
        data += s.getData(name, year, semester)
    else:
        data += s.getData(name, year, 1)
        data += s.getData(name, year, 2)
    
    if len(data)==0:
        return HttpResponse("NoneData",content_type='text/plain')
    
    heads=[]
    for i in data[0].keys():
        heads.append(i)  
    s=','.join(heads)  
    for i in data:
        s+="\n"
        s+=','.join(i.values())
    return HttpResponse(s,content_type='text/plain; charset=utf-8')

def schoolAPI2(request, *args, **kwargs):
    if request.user.username=="" or request.user.detail.type <2:
        try:
            user = Detail.objects.filter(license=kwargs['license'])
            if not user:
                return HttpResponse("LoginFail", content_type='text/plain')
        except Exception as e:
            print(e)
            return HttpResponse("LoginFail", content_type='text/plain')
    
    
    name = kwargs['name']
    startYear = int(kwargs['startYear']) if 'startYear' in kwargs else None
    endYear = int(kwargs['endYear']) if 'endYear' in kwargs else None
    semester = int(kwargs['semester']) if 'semester' in kwargs else None

    
    data = []
    s = SchoolApi()
    if semester==None:
        for i in range(startYear,endYear+1):
            #data.append(s.getData(name, i))
            data += s.getData(name, i)
    elif semester>0:
        for i in range(startYear,endYear+1):
            #data.append(s.getData(name, i, semester))
            data += s.getData(name, i, semester)
    else:
        for i in range(startYear,endYear+1):
            #data.append(s.getData(name, i, 1))
            #data.append(s.getData(name, i, 2))
            data += s.getData(name, i, 1)
            data += s.getData(name, i, 2)

    if len(data)==0:
        return HttpResponse("NoneData",content_type='text/plain')
    
    heads=[]
    for i in data[0].keys():
        heads.append(i)  
    s=','.join(heads)  
    for i in data:
        s+="\n"
        s+=','.join(i.values())

    return HttpResponse(s, content_type='text/plain; charset=utf-8')

def templateJSON(request, *args, **kwargs):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'example.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
            return JsonResponse(data,safe=False)        


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
        year = str(year) if year!=None else None
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

    def getRequest(self,url):
        isProxy = False
        
        if isProxy:
            proxies={"http":"http://ip_address_removed:3128"}
            return requests.get(url, proxies=proxies).text
        else:
            return requests.get(url).text


    def getSchoolTemp(self):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'example.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
        return []
    
    def getCSV(self, jsonData):
    # Open three threads  
    #thd1 = threading.Thread(target=doJob, name='Thd1', args=(que,))  
    #thd2 = threading.Thread(target=doJob, name='Thd2', args=(que,))  
    #thd3 = threading.Thread(target=doJob, name='Thd3', args=(que,))  
      
    # Start activity to digest queue.  
    #st = datetime.datetime.now()  
    #thd1.start()  
    #thd2.start()  
    #thd3.start()  
                
        return self.csv
    
    def ConvertCSV(self,data): 
        for i in data:
            self.csv+="\n"
            self.csv+=','.join(i.values())
