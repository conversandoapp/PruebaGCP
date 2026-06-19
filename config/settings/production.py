from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    '.appspot.com',
    '.run.app',
    os.environ.get('ALLOWED_HOST', ''),
]

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
