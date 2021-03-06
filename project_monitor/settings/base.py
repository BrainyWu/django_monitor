# -*- coding: utf-8 -*-
__author__ = 'wuhai'
"""
Django settings for project_monitor project.

Generated by'django-admin startproject'using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import logging.config
import os
from pathlib import Path
import sys
import time

# Build paths inside the project like this: BASE_DIR /'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
csv_files_path = os.path.join(BASE_DIR, "csv_files")
log_path = os.path.join(BASE_DIR, "logs")
if not os.path.exists(log_path):
    os.mkdir(log_path)
logging.config.fileConfig(os.path.join(BASE_DIR, 'conf\\logging.ini'))

sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
sys.path.insert(0, os.path.join(BASE_DIR, "celery_tasks"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dqk=gc^4bq-0x=i%0)v4hw0-ock0e=pe0#6$64x9*)o(9xd9$b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
ROOT_URLCONF = 'project_monitor.urls'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'rest_framework',
    'django_filters',
    'crispy_forms',
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

WSGI_APPLICATION = 'project_monitor.wsgi.application'

# CELERY SETTINGS
# broker 配置
CELERY_BROKER_URL = 'redis://localhost:6379/5'
# 结果保存配置
CELERY_RESULT_BACKEND = 'redis://localhost:6379/6'
CELERY_RESULT_EXPIRES = 60 * 60 * 12
CELERY_MAX_TASKS_PRE_CHILD = 10
# 序列化相关配置
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
from project_monitor.taskschedulers import beat_schedulers
CELERYBEAT_SCHEDULE = beat_schedulers

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'celery_tasks',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 100,
            }
        }
    },
    "cookie": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 100,
                # 避免转码，直接对原数据进行操作, 默认False
                "decode_responses": True,
            }
        }
    }
}

# rest framework
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'lib.exceptions.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
