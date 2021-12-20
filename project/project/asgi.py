# 라우터다 이 놈이!
# import os

# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# import main.routing
# import jychat.routing
# import webrtc.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(), # http를 처리해줘~  Just HTTP for now. (We can add other protocols later.)
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             main.routing.websocket_urlpatterns + jychat.routing.websocket_urlpatterns \
#             + webrtc.routing.websocket_urlpatterns 
#         )
#     ) # 웹 소켓을 처리해줘~
# })

# mysite/asgi.py
import os

import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing
import jychat.routing
import webrtc.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heal.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns + jychat.routing.websocket_urlpatterns \
            + webrtc.routing.websocket_urlpatterns 
        )
    ),
})
