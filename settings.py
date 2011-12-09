# Django settings for datarav project.
import os.path
APPLICATION_DIR = os.path.dirname( globals()[ '__file__' ] )

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'testdb',                      # Or path to database file if using sqlite3.
        'USER': 'testuser',                      # Not used with sqlite3.
        'PASSWORD': 'testpass',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# the django-social-auth module uses the @login_required
# decorator, which directs browsers to settings.LOGIN_URL
# after either a successful OR failed login
LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/logged-in/'
LOGIN_ERROR_URL    = '/login-error/'

AUTH_PROFILE_MODULE = "accounts.UserProfile"

#####
SOCIAL_AUTH_LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL = LOGIN_URL
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/logincomplete'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'

SOCIAL_AUTH_ERROR_KEY = 'social_errors'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

#####

SOCIAL_AUTH_IMPORT_BACKENDS = (
    'myproy.social_auth_extra_services',
)

SOCIAL_AUTH_ENABLED_BACKENDS = ('twitter', 'facebook')

TWITTER_CONSUMER_KEY         = 'OisyZvqlGOgQu8eCrA2mRw'
TWITTER_CONSUMER_SECRET      = 'HNiXDpWPT2C6ZkeO1Rtaq8GqBo5Lvvqq8ncoLLQ'
ZEO_CONSUMER_KEY             = '09AF4677D82B1511F538FAF51E69BD67'
ZEO_CONSUMER_SECRET          = '09AF4677D82B1511F538FAF51E69BD67'
TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
#"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages", 
#'social_auth.context_processors.social_auth_by_type_backends',
)


OAUTH_WITHINGS_REQUEST_TOKEN_URL = 'https://oauth.withings.com/account/request_token'
OAUTH_WITHINGS_ACCESS_TOKEN_URL = 'https://oauth.withings.com/account/access_token'
OAUTH_WITHINGS_AUTHORIZATION_URL = 'https://oauth.withings.com/account/authorize'
OAUTH_WITHINGS_CALLBACK_URL = 'http://192.168.2.7:8000/withings/request_token_ready'
OAUTH_WITHINGS_RESOURCE_URL = 'http://wbsapi.withings.net/once?action=probe'

# key and secret granted by the service provider for this consumer application - same as the MockOAuthDataStore
OAUTH_WITHINGS_CONSUMER_KEY = 'e10d1995ed26c450dd36ee65d0b3092071bb33f5496c21f25d70c792'
OAUTH_WITHINGS_CONSUMER_SECRET = '79c4fd4853cfcbf8c7f1f91156325e190bd34bddd2ed7cf4068ecf987026495'
#OAUTH_WITHINGS_CONSUMER_KEY = '1e010b6eb501002ededd305c020f776dc0d74d2947ebb1ee37321589bc5785'
#OAUTH_WITHINGS_CONSUMER_SECRET = '9c63ee28b58bccf497c019e1b9e83d73e2c263f6ed7ffb9d82f966597eb36'



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

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
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join( APPLICATION_DIR, 'resources' )

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://192.168.2.7:8000/resources/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rvbw3w7#k9nc+*c&^cs^@^r0+fepe(6t$o(x^r^&-yb_jl%9^l'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'datarava.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/Users/d43pan/dev/ve/datarava/datarava/templates",
    #os.path.join(os.path.basename(__file__), '/templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'totalday',
    'sleeprecord',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'social_auth',
    'accounts',
    'withings'

)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
#   'social_auth.backends.zeo.ZeoBackend',
#    'social_auth.backends.facebook.FacebookBackend',
#    'social_auth.backends.google.GoogleOAuthBackend',
#    'social_auth.backends.google.GoogleOAuth2Backend',
#    'social_auth.backends.google.GoogleBackend',
#    'social_auth.backends.yahoo.YahooBackend',
#    'social_auth.backends.contrib.linkedin.LinkedinBackend',
#    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
#    'social_auth.backends.contrib.orkut.OrkutBackend',
#    'social_auth.backends.contrib.foursquare.FoursquareBackend',
#    'social_auth.backends.contrib.github.GithubBackend',
#    'social_auth.backends.contrib.dropbox.DropboxBackend',
#    'social_auth.backends.contrib.flickr.FlickrBackend',
#    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'INFO',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'datarava': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }
}