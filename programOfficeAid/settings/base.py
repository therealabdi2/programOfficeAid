import os
from pathlib import Path

from decouple import config
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_interface',
    'colorfield',
    'accounts',
    'courses',
    'submissions',
    'crispy_forms',
    'import_export',
    'django_extensions',
    'django.contrib.admin',
    'rest_framework',
    'imagekit',
    'ajax_select',
    'storages',

    'django.contrib.sites',  # make sure sites is included
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# for django-admin-interface
X_FRAME_OPTIONS = 'SAMEORIGIN'
SILENCED_SYSTEM_CHECKS = ['security.W019']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.ProfileMiddleware',
]

ROOT_URLCONF = 'programOfficeAid.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
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

WSGI_APPLICATION = 'programOfficeAid.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if 'DATABASE_UR' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('ENGINE'),
            'NAME': os.environ.get('NAME'),
            'USER': os.environ.get('USER'),
            'PASSWORD': os.environ.get('PASSWORD'),
            'HOST': os.environ.get('HOST'),
            'PORT': 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Karachi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../static')
STATICFILES_DIRS = [
    'programOfficeAid/static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.Account'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

SITE_ID = 1
LOGIN_REDIRECT_URL = 'accounts:dashboard'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # existing backend
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_FORMS = {
    'login': 'accounts.forms.CustomLoginForm',
    'signup': 'accounts.forms.CustomSignupForm',
}

ACCOUNT_ADAPTER = 'accounts.adapter.ValidateEmailAdapter'

# SMTP Configuration
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)