# -*- coding: utf-8 -*- 

#
# Sample Pyerp settings base on Django settings
#

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'pyerp@yahoo.cn'),
)
MANAGERS = ADMINS

#
# SMTP server settings
#
EMAIL_HOST="mail.pyerp.cn"
EMAIL_PORT="25"
EMAIL_HOST_USER="demo@pyerp.cn"
EMAIL_HOST_PASSWORD="xxxx"
DEFAULT_FROM_EMAIL="demo@pyerp.cn"
SERVER_EMAIL="demo@pyerp.cn"

# for server unit testing
DATABASE_ENGINE = 'sqlite3'      # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
TEST_DATABASE_NAME = 'build/pyerp_testing.db' # Or path to database file if using sqlite3.

# for pc unit testing
#DATABASE_ENGINE = 'mysql'
#TEST_DATABASE_NAME = 'pyerpcn_testing'
#DATABASE_USER = 'root'
#DATABASE_PASSWORD = ''
#DATABASE_HOST = ''
#DATABASE_PORT = ''

# Strings used to set the character set and collation order for the test
# database. These values are passed literally to the server, so they are
# backend-dependent. If None, no special settings are sent 
# (system defaults are used)
TEST_DATABASE_CHARSET = 'utf8'
# TEST_DATABASE_COLLATION = None

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e-mmp#$-$#5qs37o@3755&6zaw#xuip&+-79m-q=zhd8!uzbg#'

# List of callables that know how to import templates from various sources.

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'pyerp.fnd.middleware.FndMediaMiddleware',    # using media from app's package.
    #'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pyerp.fnd.middleware.FndGlobalMiddleware', 
    #'django.middleware.transaction.TransactionMiddleware', 
    
)

#
# FEEDBACK_TRAC_NEWTICKET_URL
# using trac's root url for support or feedback.
#
FEEDBACK_TRAC_NEWTICKET_URL = 'http://code.pyerp.cn/newticket'

#
# ...
#
INTERNAL_IPS = ('127.0.0.1',)
TEMPLATE_CONTEXT_PROCESSORS = ( 
    "django.core.context_processors.debug",    #debug .........SQL.."
) 


#
# 
#
ROOT_URLCONF = 'pyerp.urls'


#
# FOR fnd.templatetags.fndtag.py
#
FND_MEDIA_PREFIX='/fnd_media/'
FND_RESP_SITE_PREFIX = 'resp/'
FND_USER_SITE_PREFIX = 'user/'
FND_PUB_SITE_PREFIX = ''

#
# override django.contrib.auth's backend
#
AUTHENTICATION_BACKENDS = ('pyerp.fnd.auth.FndUserBackend',)

INSTALLED_APPS = (
    'django.contrib.sites',         
    'django.contrib.contenttypes',  
    'django.contrib.sessions',      
    'django.contrib.auth',          
    'pyerp.fnd',
    # 'pyerp.ak',
    # 'pyerp.gl',
    # 'pyerp.ec',
    # 'pyerp.jobs',
    # 'pyerp.survey',
)


