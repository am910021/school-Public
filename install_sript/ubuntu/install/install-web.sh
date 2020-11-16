#!/bin/bash
if [[ $EUID -ne 0 ]]; then
	echo "你必需是 root 才能安裝伺服器。" 2>&1
	exit 1
else
WEBAPP=/srv/webapps/
cd $WEBAPP	
mkdir school_django/
cd school_django/
mkdir logs run media
virtualenv -p /usr/bin/python3 .
source bin/activate
pip3 install -r $WEBAPP/install/requirements.txt
deactivate
cd $WEBAPP
cd install/virtualenv/
chmod +x runserver.bash
cp runserver.bash $WEBAPP/school_django/bin/runserver.bash
cd $WEBAPP
cd install/key/
eval "$(ssh-agent -s)"
chmod 600 id_rsa
ssh-add id_rsa
cd $WEBAPP
mkdir temp
cd temp
clear
echo '第一次使用ssh Github請輸入yes'
git clone git@github.com:am910021/school.git
cd school
mv school $WEBAPP/school_django/
cd ..
rm -rf school
cd ..
rm -rf temp
cd $WEBAPP/school_django/
source bin/activate
cd school/
python manage.py collectstatic --noinput
python setup.py install
deactivate
mv static/ ../
supervisorctl reread
supervisorctl update
supervisorctl restart school
service nginx restart

fi

