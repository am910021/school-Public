"""
WSGI config for school project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# wsgi apache setting
#sys.path.append('/srv/webapps/school_django/school')
#sys.path.append('/srv/webapps/school_django/lib/python3.6/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")

application = get_wsgi_application()
