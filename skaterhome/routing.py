from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from chat.consumers import ChatConsumer
from chatx.routing import websocket_urlpatterns as chatx_url_routing

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chatx_url_routing +
                [
                    url(r"^messages/(?P<username>[\w.@+-]+)/$", ChatConsumer),

                ],
            )
        )
    )
})

# notes
# ws://domain/<username>
