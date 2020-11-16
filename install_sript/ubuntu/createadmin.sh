#!/bin/bash
if [[ $EUID -ne 0 ]]; then
	echo "你必需是 root 才能更新伺服器。" 2>&1
	exit 1
else
	WEBAPP=/srv/webapps/
	cd $WEBAPP/school_django/
	source bin/activate
	cd school/
	python setup.py createadmin
	deactivate
	exit
fi