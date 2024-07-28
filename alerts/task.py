from asgiref.sync import sync_to_async
from celery import shared_task
from django.dispatch.dispatcher import asyncio
import websockets
import json
from django.core.mail import send_mail
from django.conf import settings
from .models import Alert


def websocket_url(coin_name: str) -> str:
    return f"wss://stream.binance.com:9443/ws/{coin_name.lower()}@trade"


def get_sub_json(coin: str, idx: int):
    return json.dumps(
        {
            "method": "SUBSCRIBE",
            "params": [f"{coin.lower()}@trade"],
            "id": idx,
        }
    )


def on_message(message):
    """
    Handles incoming WebSocket messages, updates alert statuses, and sends notification emails.

    Args:
        message (str): The WebSocket message in JSON format containing trade data.
    """
    try:
        # Parse the JSON message to extract trade data
        data = json.loads(message)

        # Check if the message contains the price information
        if "p" not in data:
            return

        # Extract the price from the message
        price = float(data["p"])

        # Find all alerts where the target price is less than or equal to the current price
        alerts = Alert.objects.filter(target_price__lte=price, status="created")

        # Process each alert
        for alert in alerts:
            # Update alert status to "triggered"
            alert.status = "triggered"
            alert.save()

            print("-" * 30)
            print(
                f"Price Alert Triggered: {alert.coin} at ${price} for {alert.user.email}"
            )

            # Send an email notification to the user
            send_mail(
                subject="Price Alert Triggered",
                message=f"The price of {alert.coin} has reached your target of ${alert.target_price}!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[alert.user.email],
                fail_silently=False,
            )
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        # Log the exception if needed (optional)
        print(f"Error processing message: {e}")


async def _fetch_external_websocket_data_async():
    URI = websocket_url("btcusdt")
    async with websockets.connect(URI) as ws:
        # Subscribe to the WebSocket channel
        await ws.send(get_sub_json("btcusdt", 0))
        try:
            # Continuously listen for incoming messages
            message = await ws.recv()
            await sync_to_async(lambda: on_message(message))()
        except websockets.ConnectionClosed:
            # Handle closed connection
            print("[CLOSED] Connection closed")


@shared_task
def fetch_external_websocket_data():
    asyncio.run(_fetch_external_websocket_data_async())
