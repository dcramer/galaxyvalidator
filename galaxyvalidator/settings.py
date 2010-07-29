import os.path

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PROFILING = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('David Cramer', 'dcramer@localhost'),
    ('David Cramer', 'dcramer@gmail.com'),
)

EMAIL_FROM_ADDRESS = 'noreply@nibbits.com'

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'galaxyvalidator'
DATABASE_USER = 'galaxyvalidator'
DATABASE_PASSWORD = ''
DATABASE_HOST = 'localhost'
DATABASE_PORT = ''
DATABASE_OPTIONS = {
   "init_command": "SET storage_engine=INNODB;",
}

BASE_URL = ''
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

LAPIN_INCLUDE_PATH = os.path.join(PROJECT_ROOT, 'lapin', 'includes', 'Core.SC2Mod') 
LAPIN_BINARY_PATH = os.path.join(PROJECT_ROOT, 'lapin', 'bin', 'lapin')

JINJA2_EXTENSIONS = (
    'jinja2.ext.do',
)
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/Chicago'

# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

MEDIA_URL = '%s/media/' % (BASE_URL,)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

ADMIN_MEDIA_PREFIX = '%s/admin/media/' % (BASE_URL,)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-!^qh-_7u)_w3aoem&!10a^5r-0*fb6_ic&$wfrebm74os$)9*'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

AUTHENTICATION_BACKENDS = (
    #'nibbits.accounts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.middleware.doc.XViewMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    #'nibbits.context_processors.default',
)

ROOT_URLCONF = 'galaxyvalidator.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'galaxyvalidator.validator',
    'coffin',
)

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

DEFAULT_CHARSET = 'UTF-8'

EXTRA_INSTALLED_APPS = ()
EXTRA_MIDDLEWARE_CLASSES = ()

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_NAME = 'galaxyvalidator'

try:
    from local_settings import *
except ImportError:
    pass

LOGIN_URL = BASE_URL + '/account/login/'

SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

import logging
logging.basicConfig(
    level=DEBUG and logging.DEBUG or logging.INFO,
    #level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
)