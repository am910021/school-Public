#!/bin/sh
if ! [[ "$PWD" = */srv/webapps/* ]]; then
  echo "請把webapps.zip復製到 /srv之下後，在解壓縮執行。" 2>&1
  exit 1
fi

FILE="/srv/webapps/install/log/installed"
if [ -f "$FILE" ]; then
  echo "已經安裝過環境了，不需在安裝。" 2>&1
  exit 1
fi

RELEASE=`cat /etc/redhat-release | tr '[:lower:]' '[:upper:]'`
BRANCH="CENTOS"
VERSION="6"
if ! echo "$RELEASE" | grep -q "$VERSION" && echo "$RELEASE" | grep -q "$BRANCH"; then
  echo "你所使用的作業系統並不是CentOS 6系列。" 2>&1
  exit 1
fi

if [[ $EUID -ne 0 ]]; then
  echo "你必需是 root 才能安裝環境。" 2>&1
  exit 1
fi

WEBAPP=/srv/webapps/
curl -Lks http://www.hop5.in/yum/el6/hop5.repo > /etc/yum.repos.d/hop5.repo
yum -y install -y https://centos6.iuscommunity.org/ius-release.rpm
yum -y install https://dev.mysql.com/get/mysql57-community-release-el6-9.noarch.rpm
yum -y install epel-release gcc libxml2-devel libxslt-devel zlib-devel libstdc++ libcurl-devel libpng-devel openssl-devel python36u python36u-pip python36u-devel 
yum -y install java-1.7.0-openjdk-devel 
yum -y install java-1.7.0-openjdk
yum -y install git R nginx supervisor mysql-community-server 
yum -y install mysql-community-devel policycoreutils-python 

service mysqld restart

cd /usr/bin/
ln -s python3.6 python3
ln -s pip3.6 pip3
pip3 install --upgrade pip
pip3 install virtualenv



cd $WEBAPP	
mkdir school_django/
cd school_django/
mkdir logs run media
virtualenv -p python3 .
source bin/activate
pip3 install -r $WEBAPP/install/requirements.txt

cd $WEBAPP/install/script
python setenv.py
deactivate

rm -f tmp.sql

cd $WEBAPP
su - -c "R -e \"install.packages('https://cran.r-project.org/src/contrib/Archive/data.table/data.table_1.11.8.tar.gz', repos=NULL, type='source')\""
su - -c "R -e \"install.packages('shiny', repos='http://cran.rstudio.com/')\""
su - -c "R -e \"install.packages('RCurl', repos='http://cran.rstudio.com/')\""
su - -c "R -e \"install.packages('highcharter', repos='http://cran.rstudio.com/')\""
su - -c "R -e \"install.packages('magrittr', repos='http://cran.rstudio.com/')\""
su - -c "R -e \"install.packages('DT', repos='http://cran.rstudio.com/')\""
su - -c "R -e \"install.packages('ggplot2', repos='http://cran.rstudio.com/')\""
su - -c "R -e \"install.packages('png', repos='http://cran.rstudio.com/')\""
su - -c "R -e \"install.packages('wordcloud2', repos='http://cran.rstudio.com/')\""

yum -y install --nogpgcheck https://download3.rstudio.org/centos6.3/x86_64/shiny-server-1.5.9.923-x86_64.rpm

service mysqld stop
service supervisord stop
service nginx stop
chkconfig --add mysqld
chkconfig --add supervisord
chkconfig --add nginx
chkconfig mysqld on
chkconfig supervisord on
chkconfig nginx on


cd /var/log/nginx/
mkdir school
chown nginx:nginx school

cd /var/run/
mkdir school
chown nginx:nginx school

cd /etc/nginx/conf.d
rm -f default.conf

cd $WEBAPP/install/server/nginx/
cp school.conf /etc/nginx/conf.d/

cd /srv/
chown -R nginx:nginx shiny-server

service mysqld start
service supervisord start
service nginx start



cd $WEBAPP/install/
mkdir log
cd log
echo "installed" > installed
exit 1
