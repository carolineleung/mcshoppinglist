
# Django settings for helloWorldService project.
import logging
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# TODO Shouldn't host static files at the same path as django... what if we want them on a different host? static.other.com/
# http://docs.djangoproject.com/en/1.2/howto/static-files/
# http://docs.djangoproject.com/en/1.2/howto/deployment/modpython/#serving-media-files
STATIC_DOC_ROOT = '/static'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

currentPath = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': currentPath + '/TmpDelete.sqlite',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# MongoDB MongoEngine
from mongoengine import *
connect('mcshoppinglist', host='localhost', port=27017)


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
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

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ybup1k!$h8msvp+fe-#vk4xfjla_#xg3=y#fy0y8m#*)_h5*9&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# Original list:
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
# TODO Disabled SessionMiddleware... we don't need sessions! Unless we want Auth! "Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
#    'django.contrib.sessions.middleware.SessionMiddleware',
# TODO Enable CSRF attack prevention. http://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ref-contrib-csrf
#    'django.middleware.csrf.CsrfViewMiddleware',
# TODO Auth requires sessions
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
# TODO "The session-based temporary message storage requires session middleware to be installed, and come before the message middleware in the MIDDLEWARE_CLASSES list."
#    'django.contrib.messages.middleware.MessageMiddleware',
)

# Wrap requests in transactions
# Manually combined original with new.
# http://docs.djangoproject.com/en/1.2/topics/db/transactions/
#MIDDLEWARE_CLASSES = (
#    'django.middleware.cache.UpdateCacheMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.common.CommonMiddleware',
#    'django.middleware.transaction.TransactionMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
#)

## Wrap requests in transactions
## http://docs.djangoproject.com/en/1.2/topics/db/transactions/
#MIDDLEWARE_CLASSES = (
#    'django.middleware.cache.UpdateCacheMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.common.CommonMiddleware',
#    'django.middleware.transaction.TransactionMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',
#)


#ROOT_URLCONF = 'helloWorldService.urls'
ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #"C:/mel/hg-repo/pywebplayground/Playground/helloWorldService/templates"
    #"M:/src/_personal/hg-web/Playground/HelloWorldService/helloWorldService/templates"
    '{0}/templates'.format(currentPath)
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'shoppinglists',
    'shoppinglisteditor',
#    'tastypie',
)


# TODO Configure logging properly: http://docs.python.org/library/logging.html#configuration-dictionary-schema
LOG_FILENAME = 'myserver.log'
if os.path.isdir('/tmp'):
    LOG_FILENAME = '/tmp/' + LOG_FILENAME
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)