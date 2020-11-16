# -*- coding: utf-8 -*-
import MySQLdb, sys, os
from pip._vendor.distlib.compat import raw_input
import getpass, random, string, time

class Database:
    password = ""
    def getConnect(self) -> MySQLdb.Connection:
        return MySQLdb.connect(host="localhost", user="root", 
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

class SetSupervisord():
    def __init__(self):
        print(bcolors.OKBLUE + "執行Supervisor設定。" + bcolors.ENDC)
        self.conf = []
        
        if not self.check():
            self.loadConf()
            self.writeConf()
            print(bcolors.OKGREEN + "Supervisor設定成功。" + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "終止Supervisor設定，已設定過。" + bcolors.ENDC)
            return
            
    def writeConf(self):
        with open("/etc/supervisord.conf", "a") as file:
            for l in self.conf:
                file.write(l)
            file.close()

    def loadConf(self):
        fp = open('/srv/webapps/install/server/supervisor/school.conf', "r")
        #fp = open('/var/log/mysqld.log', "r")
        line = fp.readline()
         
        ## 用 while 逐行讀取檔案內容，直至檔案結尾
        while line:
            self.conf.append(line)
            line = fp.readline()
        fp.close()

    def check(self):
        isFound = False
        fp = open('/etc/supervisord.conf', "r")
        #fp = open('/var/log/mysqld.log', "r")
        line = fp.readline()
         
        ## 用 while 逐行讀取檔案內容，直至檔案結尾
        while line:
            if line.find("[program:school]") >=0:
                isFound = True
            line = fp.readline()
        fp.close()
        return isFound
    
class SetDatabase:
    def __init__(self):
        print(bcolors.OKBLUE + "執行MYSQL root密碼設定。" + bcolors.ENDC)
        if not self.getPwd():
            print(bcolors.FAIL + "未正常安裝MYSQL伺服器，終止密碼設定。" + bcolors.ENDC)
            return
        else:
            Database.password = self.password
            self.createSql(Database.password)
            os.system('mysql --connect-expired-password -uroot "-p%s" mysql < tmp.sql' % (Database.password))
            try:
                self.con = Database().getConnect()
            except:
                print(bcolors.FAIL + "密碼己提前變更過，終止密碼設定。" + bcolors.ENDC)
                return
            
            print(bcolors.WARNING +"===========================注意=============================")
            print("接下來執行設定MYSQL root 密碼，請誤必小心。")
            print("接下來執行設定MYSQL root 密碼，請誤必小心。")
            print("接下來執行設定MYSQL root 密碼，請誤必小心。")
            print("===========================注意============================="+ bcolors.ENDC)
            password = ""
            password2 = ""
            while(True):
                password = getpass.getpass("密碼: ")
                password2 = getpass.getpass("密碼（確認）: ")
                if password==password2:
                    break
                else:
                    print(bcolors.FAIL + "密碼不一樣,重新輸入 \n"  + bcolors.ENDC)
            self.setPwd(password)
            
    def createSql(self, pwd):
        with open("tmp.sql", "w") as file:
            file.write("set global validate_password_policy=0;\n")
            file.write("set global validate_password_length=3;\n")
            file.write("SET PASSWORD = PASSWORD('%s');\n" % (pwd))
            file.write("flush privileges;\n")
            file.close()
    
    def getPwd(self):
        isFound = False
        self.password = ""
        fp = open('/var/log/mysqld.log', "r")
        line = fp.readline()
         
        ## 用 while 逐行讀取檔案內容，直至檔案結尾
        while line:
            if line.find("A temporary password") >=0:
                self.password = line.split(": ")[1].replace("\n","")
                isFound = True
            line = fp.readline()
        fp.close()
        return isFound
    
    def setPwd(self, password):
        con = self.con
        sql1 = "set global validate_password_policy=0;"
        cursor = con.cursor()
        cursor.execute(sql1) 
        sql1 = "set global validate_password_length=3;"
        cursor = con.cursor()
        cursor.execute(sql1) 
        sql1 = "SET PASSWORD = '%s';" % (password)
        cursor = con.cursor()
        cursor.execute(sql1) 
        sql1 = "flush privileges;"
        cursor = con.cursor()
        cursor.execute(sql1) 
        con.commit()
        con.close()
        print(bcolors.OKGREEN + "MYSQL root 密碼變更成功。" + bcolors.ENDC)
        
if __name__ == "__main__":
    if os.getcwd().find("/srv/webapps") < 0:
        print(bcolors.FAIL + "請把webapps.zip復製到 /srv之下後，在解壓縮執行。" + bcolors.ENDC)
        sys.exit()
    SetDatabase()
    SetSupervisord()
    time.sleep(5)

