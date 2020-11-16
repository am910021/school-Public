#!/bin/bash
if [[ $EUID -ne 0 ]]; then
	echo "你必需是 root 才能更新伺服器。" 2>&1
	exit 1
else
	WEBAPP=/srv/webapps/
	echo "停止nginx服務中...."
	service nginx stop
	echo ""

	echo "停止supervisor服務中...."
	supervisorctl stop school
	echo ""

	cd $WEBAPP/school_django/
	rm -rf school/ static/

	cd $WEBAPP
	cd install/key/
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
	python manage.py migrate
	python manage.py collectstatic --noinput
	deactivate
	mv static/ ../
	cd ..

	echo "啟動supervisor服務中...."
	supervisorctl start school
	echo "啟動supervisor完成"

	echo "啟動nginx服務中...."
	service nginx start
	echo "啟動nginx完成"
	exit
fi
