import os
from pathlib import Path

import dj_database_url
from storages.backends.azure_storage import AzureStorage
import telebot

BASE_DIR = Path(__file__).resolve().parent.parent
NEWSLY_DIR = BASE_DIR / 'newsly'

SECRET_KEY = os.environ.get("NEWSLY_SECRET_KEY", "SUPER_SECRETY_SECRET")

DEBUG = os.environ.get("NEWSLY_DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get("NEWSLY_ALLOWED_HOST", "*").split(",")

# Those that come with the django preinstalled (and those that need to run before these)
BASE_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# External Third Party Packages
EXTERNAL_APPS = [
    'django_summernote',
    'django_q',
    'rest_framework',
    'django_filters',
]

# Apps that we wrote
CUSTOM_APPS = [
    'newsly.accounts',
    'newsly.news',
]

INSTALLED_APPS = BASE_APPS + EXTERNAL_APPS + CUSTOM_APPS

AUTH_USER_MODEL = "accounts.CustomUser"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(NEWSLY_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(),
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

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATICFILES_DIRS = (
    os.path.join(NEWSLY_DIR, 'static'),
)

if not DEBUG:
    class PublicAzureStorage(AzureStorage):
        account_name = 'unimy'
        account_key = os.environ.get('AZURE_ACCOUNT_KEY')
        azure_container = 'newsly'
        expiration_secs = None


    DEFAULT_FILE_STORAGE = 'config.settings.PublicAzureStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "Newsly",
    "site_header": "Newsly",
    "site_brand": "Newsly",
    "site_logo": "img/logo.png",
    "login_logo": "img/logo.png",
    "login_logo_dark": "img/logo.png",
    "site_logo_classes": "",
    "site_icon": "img/logo.png",
    "welcome_sign": "Newsly: News Revamped.",
    "copyright": "Newsly",
    "search_model": "accounts.CustomUser",
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Support", "url": "mailto://dev@asaurav.com.np", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": "css/admin_custom.css",
    "custom_js": "smart-selects/admin/js/chainedfk.js",
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    }
}

SUMMERNOTE_CONFIG = {
    'width': '100%',
    'toolbar': [
        ['font', ['fontname', 'fontsize', 'hr']],
        ['font', ['bold', 'underline', 'italic', 'strikethrough', 'superscript', 'subscript', 'clear']],
        ['color', ['color']],
        ['para', ['paragraph']],
        ['table', ['table']],
        ['insert', ['link', 'picture', 'video', 'line']],
        ['view', ['fullscreen']],
        ['undo', ['undo', 'redo']],
    ],
}

Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 4,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "True") == "True"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "465"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

CSRF_TRUSTED_ORIGINS = ['https://newsly.asaurav.com.np']
CORS_ORIGIN_ALLOW_ALL = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

IBM_WATSON_TTS_URL = os.environ.get("IBM_WATSON_TTS_URL", "")
IBM_WATSON_TTS_AUTHORIZATION = os.environ.get("IBM_WATSON_TTS_AUTHORIZATION", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_BOT = telebot.TeleBot(TG_BOT_TOKEN, parse_mode=None)
