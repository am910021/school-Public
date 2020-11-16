# -*- coding: utf-8 -*-
import MySQLdb, sys, os
from pip._vendor.distlib.compat import raw_input
import getpass

class Database:
    address = "127.0.0.1"
    user = "root"
    password = ""
    database = "mysql"
    
    def getConnect(self) -> MySQLdb.Connection:
        return MySQLdb.connect(host="127.0.0.1", user="root", 
                               passwd=Database.password, db="mysql", 
                               port = 3306);

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
        


    
class SetSchoolDatabase:
    def __init__(self):
        print(bcolors.OKBLUE + "執行IR資料庫設定。" + bcolors.ENDC)
        password = getpass.getpass("請輸入MYSQL root密碼: ")
        Database.password = password
        con = None
        try:
            con = Database().getConnect()
        except:
            print(bcolors.FAIL + "MYSQL root密碼錯誤。" + bcolors.ENDC)
            sys.exit()
        
        

        sql = "set global validate_password_policy=0;"
        cursor = con.cursor()
        cursor.execute(sql) 
        
        sql = "set global validate_password_length=3;"
        cursor = con.cursor()
        cursor.execute(sql) 
        
        sql = "CREATE USER 'school'@'localhost' IDENTIFIED by 'school';"
        cursor = con.cursor()
        cursor.execute(sql) 
        
        sql = "GRANT USAGE ON *.* TO 'school'@'localhost' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;"
        cursor = con.cursor()
        cursor.execute(sql) 
        
        sql = "CREATE DATABASE IF NOT EXISTS `school` default character set utf8;"
        cursor = con.cursor()
        cursor.execute(sql) 
        
        sql = "GRANT ALL PRIVILEGES ON `school`.* TO 'school'@'localhost';"
        cursor = con.cursor()
        cursor.execute(sql) 
        
        sql = "GRANT ALL PRIVILEGES ON `school\_%`.* TO 'school'@'localhost';"
        cursor = con.cursor()
        cursor.execute(sql) 
        con.commit()
        con.close()
        print(bcolors.OKGREEN + "IR資料庫設定成功。" + bcolors.ENDC)
    
if __name__ == "__main__":
    if os.getcwd().find("/srv/webapps") < 0:
        print(bcolors.FAIL + "請把webapps.zip復製到 /srv之下後，在解壓縮執行。" + bcolors.ENDC)
        sys.exit()
    SetSchoolDatabase()
