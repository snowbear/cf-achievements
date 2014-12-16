from .settings_common import *

SECRET_KEY = '3iy-!-d$!pc_ll$#$elg&cpr@*tfn-d5&n9ag=)%#()t$$5%5^'

DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

DEBUG = TEMPLATE_DEBUG = True
    
WSGI_APPLICATION = 'gettingstarted.wsgi_local.application'
