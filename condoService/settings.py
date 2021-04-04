"""
Django settings for condoService project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'XXX'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'farm.apps.FarmConfig',
    'taskEngine.apps.TaskengineConfig',
    # Django REST framework
    'rest_framework',
    # CORS
    'corsheaders',
]

REDIS_PASSWORD = 'XXX'

REDIS_HOST = 'XXX'

CELERY_BROKER_URL = 'XXX'

MIDDLEWARE = [
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'condoService.urls'

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

WSGI_APPLICATION = 'condoService.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'CLIENT': {
            'name': 'plantCondo',
            'host': 'XXX',
            'username': 'plantCondo',
            'password': '4dQpfflzcphYBXBh',
            'authMechanism': 'SCRAM-SHA-1',
        }

    }
}

HIVEMQ_USERNAME = 'plantCondo'

HIVEMQ_PASSWORD = '!9KWdW#egQ7ch8L'

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

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8081',
)

LEVEL_0 = 0
LEVEL_1 = 1
LEVEL_2 = 2
LEVEL_3 = 3
LEVEL_4 = 4

LEVEL_0_NAME = 'Service Level'
LEVEL_1_NAME = 'Plant Level 1'
LEVEL_2_NAME = 'Plant Level 2'
LEVEL_3_NAME = 'Plant Level 3'
LEVEL_4_NAME = 'Plant Level 4'

LEVEL_CHOICES = [
    (LEVEL_0, LEVEL_0_NAME),
    (LEVEL_1, LEVEL_1_NAME),
    (LEVEL_2, LEVEL_2_NAME),
    (LEVEL_3, LEVEL_3_NAME),
    (LEVEL_4, LEVEL_4_NAME),
]

TASK_WATERING = 'WT'
TASK_SEEDING = 'SD'
TASK_PLANT_DATA_GATHERING = 'PD'
TASK_AMBIENT_DATA_GATHERING = 'AD'
TASK_MANUAL_CONTROL = 'MC'
TASK_LIGHTING_CONTROL = 'LC'

TASK_CHOICES = [
    (TASK_WATERING, 'Watering Task'),
    (TASK_SEEDING, 'Seeding Task'),
    (TASK_PLANT_DATA_GATHERING, 'Plant Data Gathering Task'),
    (TASK_AMBIENT_DATA_GATHERING, 'Ambient Data Gathering Task'),
    (TASK_MANUAL_CONTROL, 'Manual Control Task'),
    (TASK_LIGHTING_CONTROL, 'Lighting Control Task'),
]

TASK_STATUS_QUEUED = 'QED'
TASK_STATUS_EXECUTING = 'EXE'
TASK_STATUS_FINISHED = 'FIN'
TASK_STATUS_FAILED = 'FAL'

TASK_STATUS_CHOICES = [
    (TASK_STATUS_QUEUED, 'Task Queued'),
    (TASK_STATUS_EXECUTING, 'Executing'),
    (TASK_STATUS_FINISHED, 'Task Finished'),
    (TASK_STATUS_FAILED, 'Task Failed')
]

MAX_LEVEL = 1
WATERING_TASK_THRESHOLD = 10
MAX_RADIUS = 32.0
# run every DATA_GATHERING_TASK_FREQUENCY hours
DATA_GATHERING_TASK_FREQUENCY = '1'
