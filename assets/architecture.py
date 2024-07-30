from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Users 
from diagrams.onprem.database import PostgreSQL 
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis 
from diagrams.onprem.queue import Celery 
from diagrams.programming.framework import Django 
from diagrams.oci.monitoring import Email

with Diagram("Email Notfication System", show=True):
    users = Users("Users")
    django = Django("Django")
    db = PostgreSQL("Database")
    server = Server("wss://stream.binance.com")
    mail = Email("Email")
    
    with Cluster("Async workers"): 
        celery = Celery("Celery workers")
        redis = Redis("Broker")
        celery >> Edge(label="FETCH task") >> redis
        celery << redis

    django >> db 
    django << db

    db >> celery

    celery >>  server
    server >> Edge(label="FETCH price")  >> celery

    celery >> Edge(label="SEND email") >> mail

    users >> django

