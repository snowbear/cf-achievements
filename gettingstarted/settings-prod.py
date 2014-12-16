SECRET_KEY = os.environ.get('SECRET_KEY')

import dj_database_url
DATABASES['default'] =  dj_database_url.config()

WSGI_APPLICATION = 'gettingstarted.wsgi-cling.application'

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
