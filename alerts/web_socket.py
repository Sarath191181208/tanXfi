
import websocket
import json
from django.core.mail import send_mail
from django.conf import settings
from .models import Alert

def on_message(ws, message):
    data = json.loads(message)
    price = float(data['p'])
    alerts = Alert.objects.filter(target_price__lte=price, status='created')
    for alert in alerts:
        alert.status = 'triggered'
        alert.save()
        send_mail(
            'Price Alert Triggered',
            f'The price of {alert.coin} has reached your target of ${alert.target_price}!',
            settings.EMAIL_HOST_USER,
            [alert.user.email],
            fail_silently=False,
        )

def on_error(ws, error):
    print(f'Error: {error}')

def on_close(_: websocket.WebSocket, *args):
    print('### closed ###')

def on_open(ws):
    ws.send(json.dumps({'method': 'SUBSCRIBE', 'params': ['btcusdt@trade'], 'id': 1}))

def run_websocket():
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@trade",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
