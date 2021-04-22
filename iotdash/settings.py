
import  os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fsfs@4%mskd%s9sec1qf1$v*ix1_6lo-1iyapjahausdh3n2a3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['206.189.128.29','adhocdevices.com','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dash',
    'paypal.standard.ipn',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
            ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

ROOT_URLCONF = 'iotdash.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'iotdash.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_URL = '/signupLogin/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'dash/static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
PAYPAL_RECEIVER_EMAIL = 'XXXXX@gmail.com'

PAYPAL_TEST = True

# Email Configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

EMAIL_HOST_USER = 'YOUR-EMAIL'
EMAIL_HOST_PASSWORD = 'YOUR-EMAIL-PASSWORD'
# "eab641ca2b95dad47986451dcf0f940796f3d140"

# AWS Configuration
# AWS_ACCESS_KEY_ID = ''  # Your AWS Access Key ID
# AWS_SECRET_ACCESS_KEY = ''  # Your AWS Secret Access Key
# AWS_STORAGE_BUCKET_NAME = 'adhoc-devices'  # Your AWS Bucket name
#
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# #
# #
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_CLOUDFRONT_DOMAIN = 'd5t9gpjcr1j5s.cloudfront.net'
# AWS_S3_OBJECT_PARAMETERS = {
#      'CacheControl': 'max-age=86400',
# }
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
#
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
#
# STATICFILES_LOCATION = 'static'
# STATIC_ROOT = '/%s/' % STATICFILES_LOCATION
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CLOUDFRONT_DOMAIN, STATICFILES_LOCATION)
# # STATIC_URL = 'https://%s/static/' % AWS_S3_CLOUDFRONT_DOMAIN
#
# MEDIAFILES_LOCATION = '/media/static/img1'
# MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CLOUDFRONT_DOMAIN, MEDIAFILES_LOCATION)
# MEDIA_ROOT = MEDIA_URL
# # MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
