"""

Local development Django settings for dhmit/tobacco_networks

Under no circumstances run the server with these settings in production!

"""

from .base import *  # pylint: disable=unused-wildcard-import, wildcard-import


SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'dual-momentum.com',
]

CORS_ORIGIN_ALLOW_ALL = True
