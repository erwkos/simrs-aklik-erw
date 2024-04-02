"""
ASGI config for pengaturan project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# import websocket.start_server

#export DJANGO_SETTINGS_MODULE=home.chikal.Documents.viis.viis.settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'viis.settings')

application = get_asgi_application()

#app = get_asgi_application()

#application = ProtocolTypeRouter({
#    "http": get_asgi_application(),
#    "websocket": AuthMiddlewareStack(
#        URLRouter(websocket_path)
#    )
#})

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": URLRouter(websocket_path)
# })
