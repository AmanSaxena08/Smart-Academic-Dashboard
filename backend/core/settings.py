from pathlib import Path
from datetime import timedelta
import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured


def _csv_env(name, default):
    """Read a comma-separated env var into a clean list."""
    return [v.strip() for v in os.environ.get(name, default).split(',') if v.strip()]


BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ──────────────────────────────────────────────────
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Never ship a real key in source. Production must supply one.
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'django-insecure-local-dev-key-not-for-production'
    else:
        raise ImproperlyConfigured(
            'SECRET_KEY must be set as an environment variable when DEBUG=False.'
        )

ALLOWED_HOSTS = _csv_env(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,.onrender.com' if DEBUG else '.onrender.com'
)

CSRF_TRUSTED_ORIGINS = _csv_env(
    'CSRF_TRUSTED_ORIGINS',
    'https://smart-academic-dashboard-hi7g.onrender.com,'
    'https://smart-academic-frontend.onrender.com'
)

# ── Installed Apps ────────────────────────────────────────────
INSTALLED_APPS = [
    'jazzmin',  # must precede django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'users',
    'academics',
    'attendance',
    'resources',
    'exams',
    'notifications',
    'notices',
]

# ── Middleware ────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ── Database ──────────────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # dj-database-url expects the postgres:// scheme.
    if DATABASE_URL.startswith('postgresql://'):
        DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgres://', 1)
    # Managed Postgres (Neon, Supabase, Render) requires TLS.
    if 'sslmode=' not in DATABASE_URL:
        DATABASE_URL += ('&' if '?' in DATABASE_URL else '?') + 'sslmode=require'
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            # Serverless Postgres suspends idle connections. Without this,
            # Django reuses a dead socket and throws OperationalError on the
            # first request after the database wakes up.
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ── Auth ──────────────────────────────────────────────────────
AUTH_USER_MODEL = 'users.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── REST Framework ────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# ── JWT ───────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ── CORS ──────────────────────────────────────────────────────
# Wide open locally for convenience; explicit allowlist in production.
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = _csv_env(
    'CORS_ALLOWED_ORIGINS',
    'https://smart-academic-frontend.onrender.com'
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ── Internationalization ──────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# ── Media Files ───────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ── Jazzmin Admin Theme ─────────────────────────────────────────
JAZZMIN_SETTINGS = {
    'site_title': 'Smart Academic Admin',
    'site_header': 'Smart Academic Dashboard',
    'site_brand': 'Smart Academic',
    'welcome_sign': 'Smart Academic Dashboard — Administration',
    'copyright': 'Smart Academic Dashboard',
    'search_model': ['users.CustomUser', 'academics.Subject'],
    'show_ui_builder': False,
    'changeform_format': 'horizontal_tabs',
    'icons': {
        'users.CustomUser': 'fas fa-user',
        'users.StudentProfile': 'fas fa-user-graduate',
        'users.FacultyProfile': 'fas fa-chalkboard-teacher',
        'academics.Department': 'fas fa-building',
        'academics.Subject': 'fas fa-book',
        'academics.Section': 'fas fa-users',
        'academics.Timetable': 'fas fa-calendar-alt',
        'attendance.AttendanceSession': 'fas fa-clipboard-check',
        'attendance.AttendanceRecord': 'fas fa-check-double',
        'resources.Resource': 'fas fa-file-alt',
        'exams.Exam': 'fas fa-file-signature',
        'exams.ExamResult': 'fas fa-poll',
        'notifications.Notification': 'fas fa-bell',
        'notices.Notice': 'fas fa-bullhorn',
    },
}

JAZZMIN_UI_TWEAKS = {
    'navbar': 'navbar-navy navbar-dark',
    'sidebar': 'sidebar-dark-navy',
    'accent': 'accent-navy',
    'brand_colour': 'navbar-navy',
    'theme': 'default',
    'dark_mode_theme': None,
    'sidebar_nav_flat_style': True,
    'button_classes': {
        'primary': 'btn-primary',
        'success': 'btn-success',
        'danger': 'btn-danger',
    },
}
