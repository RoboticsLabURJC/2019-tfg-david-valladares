from channels.routing import route
from jderobot_server.consumers import SimConsumer

channel_routing = [
    SimConsumer.as_route(),
]
# channel_routing = {
#     "websocket.connect": "jderobot_server.consumers.websocket_connect",
#     "websocket.keepalive": "jderobot_server.consumers.websocket_keepalive",
#     "websocket.disconnect": "jderobot_server.consumers.websocket_disconnect",
#     "websocket.receive" : "jderobot_server.consumers.websocket_recive",
# }

ASGI_APPLICATION = "jderobot_server.routing.application"

