from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres_local',
        'USER':'postgres',
        'PASSWORD':'vicky0607',
    }
}
