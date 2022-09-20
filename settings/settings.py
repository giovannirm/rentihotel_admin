import os
import datetime
import environ
from django.conf import settings
import redis

env = environ.Env( # set casting, default value
   DEBUG=(bool, False)
   #DEBUG=(bool, True)
)
# reading .env file
environ.Env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#DEBUG = True
USE_DJANGO_JQUERY = True

ALLOWED_HOSTS = ['localhost','127.0.0.1','www.rentihotel.com','rentihotel.com','apirenti.com','www.apirenti.com','rentigestion.com','www.rentigestion.com']

CORS_ORIGIN_WHITELIST = ("localhost:3000","www.rentihotel.com","rentihotel.com","www.rentigestion.com","rentigestion.com")
CORS_ALLOW_CREDENTIALS = True

#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True

#CSRF_TRUSTED_ORIGINS = ("localhost:3000",)
#SESSION_COOKIE_DOMAIN="127.0.0.1"

#CORS_REPLACE_HTTPS_REFERER = True
CSRF_TRUSTED_ORIGINS = ["rentihotel.com","localhost",'127.0.0.1',"rentigestion.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',    
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'grappelli dashboard',
    'grappelli',

    #rest framework
    'rest_framework',

    # Optional utilities:
    'corsheaders',
    
    #social    
    'social_django',

    # Your apps here:
    'cliente',
    'departamento',
    'distrito',    
    'habitacion',
    'hospedante',
    'hotel',
    'pagoculqi',
    'pais',
    'parametro',
    'adicional',
    'provincia',
    'registrocliente',
    'registro',
    'registrohabitacion',
    'registroadicional',
    'reserva',
    'reservadetalle',
    'servicio',   
    'tiempo',
    'tipohabitacion',   
    'usuario',

    #documentacion
    'rest_framework_swagger',     

]

AUTH_USER_MODEL = 'usuario.User'

MIDDLEWARE = [
    #'django.middleware.cache.UpdateCacheMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'utils.middleware.ValidateTokenMiddleware',
    'django.middleware.security.SecurityMiddleware',   
    'django.contrib.sessions.middleware.SessionMiddleware',     
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',    
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'yopvtpjr',
        'USER': 'yopvtpjr',
        'PASSWORD': '8IbFOjAB4nxQW9Ald0cGfk5MQnWEFLBE',
        'HOST': 'salt.db.elephantsql.com',
        'PORT': '',
    },
}


'''
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'DEBUG/debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            #'propagate': True,
        },
    },
}
'''

# REDIS
redis_connection = redis.Redis(host='localhost', port=6379, db=1)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/


LANGUAGE_CODE = 'es-PE'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

GRAPPELLI_ADMIN_TITLE = 'Renti'

BASE_URL = ''


PASSWORD_RESET_TIMEOUT_DAYS=1

JWT_AUTH = {     
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=6),
    #'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=200),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),

    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_AUTH_COOKIE': None,

}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

    'DEFAULT_PERMISSION_CLASSES':(
        'rest_framework.permissions.IsAuthenticated',        
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (        
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),

    'DEFAULT_PAGINATION_CLASS': 'drf_link_header_pagination.LinkHeaderPagination',
    'PAGE_SIZE': 10
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

### SOCIAL AUTENTICATION

#SOCIAL_AUTH_URL_NAMESPACE = 'social'
WHITELISTED_DOMAINS = ['hotmail.com', 'gmail.com']
#LOGIN_REDIRECT_URL = '//'
#SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
#SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://localhost:3000/lista'


SOCIAL_AUTH_USER_MODEL = 'usuario.User'
SOCIAL_AUTH_FACEBOOK_KEY = env('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.mail.mail_validation',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.debug.debug',
)


###MAILS 

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
PASSWORD_RESET_TIMEOUT_DAYS = 1

DEFAULT_FROM_EMAIL = 'renti0126@gmail.com'
SERVER_EMAIL = 'renti0126@gmail.com'

DEFAULT_FROM_EMAIL = 'Renti Team <renti0126@gmail.com>' 
#SERVER_EMAIL = 'renti0126@gmail.com'


#CULQUI
CULQI_PRIVATE_KEY = env('CULQI_PRIVATE_KEY')