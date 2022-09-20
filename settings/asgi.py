"""
ASGI config for settings project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PATHS = [os.path.realpath(os.path.join(BASE_DIR, 'apps'))]
for path in PATHS:
    sys.path.insert(0, path)

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')


application = get_asgi_application()
