from .settings_common import *

ADMINS = [ ('Marat Yuldashev', 'marat.snowbear@gmail.com') , ('CFA robot', 'cfa.yuldashev@gmail.com') ]
MANAGERS = [ ('CFA robot', 'cfa.yuldashev@gmail.com') ]
SERVER_EMAIL = 'cfa.yuldashev@gmail.com'
DEFAULT_FROM_EMAIL = 'cfa.yuldashev@gmail.com'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "cfa.yuldashev"
EMAIL_HOST_PASSWORD = os.environ.get('CFA_EMAIL_ACCOUNT_PASSWORD')
EMAIL_USE_TLS = True

SECRET_KEY = os.environ.get('CFA_SECRET_KEY')

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'cf_achievements',
    'USER': 'postgres',
    'PASSWORD': os.environ.get('CFA_DB_PASS_PROD'),
    'HOST': 'localhost',
    'PORT': '',
}

STATIC_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = '/var/www/cfa'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(STATIC_BASE_DIR, 'static'),
)
