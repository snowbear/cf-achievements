from .settings_common import *

SECRET_KEY = '3iy-!-d$!pc_ll$#$elg&cpr@*tfn-d5&n9ag=)%#()t$$5%5^'

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'cf_achievements',
    'USER': 'cf_achievements',
    'PASSWORD': 'cfa',
    'HOST': 'localhost',
    'PORT': '',
}

DEBUG = TEMPLATE_DEBUG = True
    
WSGI_APPLICATION = 'gettingstarted.wsgi_local.application'
