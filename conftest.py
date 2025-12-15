import os
import django
from django.conf import settings
from django.core.management import call_command

def pytest_configure():
    """Configure Django settings for pytest."""
    settings.configure(
        DEBUG=True,
        SECRET_KEY='test-secret-key-for-dj-paynow-testing',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'paynow',
        ],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        ROOT_URLCONF='tests.urls',
        TEMPLATES=[{
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
        }],
        USE_TZ=True,
        DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
        
        # PayNow settings
        PAYNOW_INTEGRATION_ID='test_integration_id',
        PAYNOW_INTEGRATION_KEY='test_integration_key',
        PAYNOW_TEST_MODE=True,
    )
    
    django.setup()
    
    # Create database tables
    call_command('migrate', '--run-syncdb', verbosity=0, interactive=False)