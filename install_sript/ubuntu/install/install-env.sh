#!/bin/bash
if [[ $EUID -ne 0 ]]; then
	echo "你必需是 root 才能安裝環境。" 2>&1
	exit 1
else
WEBAPP=/srv/webapps/
apt-get update
if [[ $? > 0 ]]
then
    echo "apt-get 指令錯誤，請重新輸入指令，或是重開機後重試指令。"
    exit
else
    echo "apt-get 狀態良好，即將進行安裝。"
fi
apt-get -y upgrade
apt-get -y install libmysqlclient-dev virtualenv python3-pip nginx supervisor mysql-server r-base r-base-dev gdebi-core libcurl4-openssl-dev libxml2-dev git
systemctl enable supervisor.service
service supervisor restart

service nginx stop
service supervisor stop
rm /etc/nginx/nginx.conf
cd $WEBAPP/install/server/nginx/
cp nginx.conf /etc/nginx/
cd $WEBAPP/install/server/supervisor/
cp school.conf /etc/supervisor/conf.d/
service supervisor start
# 更新電腦和安裝基本套件完成

su - -c "R -e \"install.packages('shiny', repos='http://cran.rstudio.com/')\""
su - -c "R -e \"install.packages('RCurl', repos='http://cran.rstudio.com/')\""
su - -c "R -e \"install.packages('highcharter', repos='http://cran.rstudio.com/')\""
su - -c "R -e \"install.packages('magrittr', repos='http://cran.rstudio.com/')\""
su - -c "R -e \"install.packages('DT', repos='http://cran.rstudio.com/')\""
su - -c "R -e \"install.packages('ggplot2', repos='http://cran.rstudio.com/')\""
wget https://download3.rstudio.org/ubuntu-12.04/x86_64/shiny-server-1.4.2.786-amd64.deb
clear
echo '安裝Shiny-Server，請輸入 yes'
gdebi shiny-server-1.4.2.786-amd64.deb
rm shiny-server-1.4.2.786-amd64.deb
rm /etc/systemd/system/shiny-server.service
cd $WEBAPP/install/server/shiny/
cp shiny-server.service /etc/systemd/system/
systemctl daemon-reload
service shiny-server restart
cd /srv/shiny-server/
mkdir apps/
cd $WEBAPP
chmod 700 update.sh
chmod +x update.sh
# 安裝Shiny Server和R會用到的套件完成
clear
echo '即將進入Mysql，接下來指令請依照手冊中的令輸入。'
echo '請輸入密碼:'
mysql -u root -p
echo '環境建立完成，請執行install-web.sh'

fi

