#!/bin/bash
if ! [[ "$PWD" = */srv/webapps/* ]]; then
  echo "請把webapps.zip復製到 /srv之下後，在解壓縮執行。" 2>&1
  exit 1
fi

FILE="/srv/webapps/install/log/installed"
if ! [ -f "$FILE" ]; then
  echo "請先執行install-env.sh，安裝好環境後在執行該腳本。" 2>&1
  exit 1
fi

if [[ $EUID -ne 0 ]]; then
  echo "你必需是 root 才能安裝伺服器。" 2>&1
  exit 1
fi
WEBAPP=/srv/webapps/
source $WEBAPP/school_django/bin/activate
cd $WEBAPP/install/script
python setweb.py
deactivate

cd $WEBAPP/install/virtualenv/
chmod +x runserver.bash
cp runserver.bash $WEBAPP/school_django/bin/runserver.bash
cd $WEBAPP/install/key/
eval "$(ssh-agent -s)"
chmod 600 id_rsa
ssh-add id_rsa
cd $WEBAPP
mkdir temp
cd temp

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
service supervisord restart
service nginx restart

semanage permissive -a httpd_t 




