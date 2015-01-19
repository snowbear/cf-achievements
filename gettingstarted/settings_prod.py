from .settings_common import *

SECRET_KEY = os.environ.get('CFA_SECRET_KEY')

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'cf_achievements',
    'USER': 'postgres',
    'PASSWORD': os.environ.get('CFA_DB_PASS_PROD'),
    'HOST': 'localhost',
    'PORT': '',
}

WSGI_APPLICATION = 'gettingstarted.wsgi_cling.application'

STATIC_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = '/var/www/cfa'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(STATIC_BASE_DIR, 'static'),
)
