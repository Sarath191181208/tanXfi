"""
This file sets up and configures a Celery worker 
for handling background tasks in a Django application.
Specifically, it is responsible for managing asynchronous 
tasks related to fetching external data via WebSocket connections.
"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'price_alert.settings')

app = Celery('alerts.task.fetch_external_websocket_data')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(["alerts.task"])

