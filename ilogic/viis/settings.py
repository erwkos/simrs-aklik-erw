"""
Django settings for viis project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)0w^h%8^gw_omp@_2*@xw^=p@w8cvds5!o%!s()#1a24_05d3i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# nambahini
CSRF_TRUSTED_ORIGINS = ['https://*.127.0.0.1']

# Application definition

INSTALLED_APPS = [
    # nambahini
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # app
    'user',
    'klaim',
    'faskes',
    'verifikator',
    'staff',
    'monitoring',
    'dokumentasi',
    'supervisor',
    'supervisorkp',
    'vpkaak',
    'metafisik',

    # modules
    'import_export',
    'crispy_forms',
    'crispy_bootstrap5',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'captcha',
    'django.contrib.humanize',
    'dal',
    'dal_select2',

    # session
    # 'django.contrib.sessions',
    'single_session',

    # user-agent
    'django_user_agents',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # klaim count
    'klaim.middleware.DaftarClaimCount',

    # session
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddlware'

    # user-agent
    'django_user_agents.middleware.UserAgentMiddleware',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'viis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# nambahini
# WSGI_APPLICATION = 'viis.wsgi.application'
ASGI_APPLICATION = 'viis.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'timeout': 30,
        }
    },

    # 'integrasi': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR + db + 'db.sqlite3',
    # }
}

# DATABASES = {
#         'default': {
#             'ENGINE': 'mssql',
#             'NAME': 'dat_ilogic',
#             'USER': 'sa',
#             'PASSWORD': 'P@ssw0rd',
#             'HOST': 'localhost',
#             'PORT': '',
#             'OPTIONS': {
#                 'driver': 'ODBC Driver 17 for SQL Server',
#             },
#         },
#     }

DATABASE_ROUTERS = [
    "dokumentasi.routers.ProgressVersionRouter",
    # "dokumentasi.routers.PolaRulesRouter",
]

# set this to False if you want to turn off pyodbc's connection pooling
DATABASE_CONNECTION_POOLING = False

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
    {
        'NAME': 'user.validators.NumberValidator',
    },
    {
        'NAME': 'user.validators.UppercaseValidator',
    },
    {
        'NAME': 'user.validators.LowercaseValidator',
    },
    {
        'NAME': 'user.validators.SymbolValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# ngubahini
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'user.User'


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = '/user/login'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# session cookie
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_SAMESITE = "Lax"

# CSRF cookie
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
# CSRF_COOKIE_AGE = None


# session logout automatis
SESSION_COOKIE_AGE = 60000
SESSION_SAVE_EVERY_REQUEST = True

# captcha size
CAPTCHA_IMAGE_SIZE = [120, 50]
CAPTCHA_FONT_SIZE = 30

try:
    from .local_settings import *
except ImportError:
    pass

