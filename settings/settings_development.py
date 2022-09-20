# coding:utf-8
from settings import *

#renti_dev
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jimmqbyh',
        'USER': 'jimmqbyh',
        'PASSWORD': 'N-Y81ltFkQ6748yTId2f3__oIW26AlI7',
        'HOST': 'raja.db.elephantsql.com',
        'PORT': '',
    },
}



DEBUG = True

BASE_URL = 'http://localhost:8000'

'''
#renti-hotel
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ubfqrzhs',
        'USER': 'ubfqrzhs',
        'PASSWORD': '5XB9uB01EHbSMtmOSu2cBRafWybTXS4c',
        'HOST': 'rajje.db.elephantsql.com',
        'PORT': '',
    },
}

'''