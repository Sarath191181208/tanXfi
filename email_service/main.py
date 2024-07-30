from mail_sender import get_smtp_config, send_email

import random
from json import loads

import redis
import config


def redis_db():
    db = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB_NUMBER,
        # password=config.REDIS_PASSWORD,
        decode_responses=True,
    )

    db.ping()
    return db


def redis_queue_push(db: redis.Redis, msg):
    db.lpush(config.REDIS_QUEUE_NAME, msg)


def redis_queue_pop(db: redis.Redis) -> str:
    _, msg_json = db.brpop(config.REDIS_QUEUE_NAME)
    return msg_json


def process_msg(db, msg_json, smtp_config):
    msg = loads(msg_json)
    print(f"Processing message {msg['id']} with data {msg['data']}")
    data = msg['data']
    coin = data.get("coin")
    price = data.get("price")
    target_price = data.get("target_price")
    email = data.get("email")
    try:
        send_email(
            "Price Alert Triggered",
            f"The price of {coin} has reached your target of ${target_price}!",
            "vssarathc04@gmail.com",
            [email],
            smtp_config,
        )
    except:
        print("Processing failed")
        redis_queue_push(db, msg_json)


def main():
    db = redis_db()
    smtp_config = get_smtp_config()
    while True:
        msg_json = redis_queue_pop(db)
        process_msg(db, msg_json, smtp_config)


if __name__ == "__main__":
    main()
