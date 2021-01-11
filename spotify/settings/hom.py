import os

from .base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "postgres",
        'USER': "postgres",
        'PASSWORD': 'spotify_base_2021',
        'HOST': 'databaseapi.cafan7lnuthi.us-west-2.rds.amazonaws.com',
        'PORT': 5432
    }
}
