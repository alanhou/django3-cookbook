from ._base import *
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings.dev')
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WEBSITE_URL = "http://127.0.0.1:8000"  # without trailing slash
MEDIA_URL = f"{WEBSITE_URL}/media/"