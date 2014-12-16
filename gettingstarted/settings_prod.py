from .settings_common import *

SECRET_KEY = os.environ.get('SECRET_KEY')

import dj_database_url
DATABASES['default'] =  dj_database_url.config()

WSGI_APPLICATION = 'gettingstarted.wsgi_cling.application'

STATIC_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(STATIC_BASE_DIR, 'static'),
)
