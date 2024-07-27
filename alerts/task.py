from asgiref.sync import sync_to_async
from celery import shared_task
from django.dispatch.dispatcher import asyncio
import websockets
import json
from django.core.mail import send_mail
from django.conf import settings
from .models import Alert

def on_message(message):
    data = json.loads(message)
    if not 'p' in data: 
        return 
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

async def _fetch_external_websocket_data_async():
    uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({'method': 'SUBSCRIBE', 'params': ['btcusdt@trade'], 'id': 1}))
        while True:
            message = await ws.recv()
            await sync_to_async(lambda: on_message(message))()

@shared_task 
def fetch_external_websocket_data():
    asyncio.run(_fetch_external_websocket_data_async())
