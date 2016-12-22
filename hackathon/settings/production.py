from .defaults import *

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT' : 5432,
    }
}
ALLOWED_HOSTS = ['*', ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'production_console': {
            'level':'INFO',
            'class':'logging.StreamHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['production_console', ]
        }
    }
}
