import os
import json
import logging
from confluent_kafka import Consumer, KafkaError

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Konfiguracja konsumenta Kafka
konfiguracja_konsumenta = {
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS', 'localhost:9092'),
    'group.id': 'moja_grupa',
    'auto.offset.reset': 'earliest'
}
konsument = Consumer(konfiguracja_konsumenta)
konsument.subscribe(['default_topic'])

async def konsumuj_wiadomosci():
    while True:
        msg = konsument.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                logger.error(msg.error())
                break
        wiadomosc = json.loads(msg.value().decode('utf-8'))
        logger.info(f'Skonsumowana wiadomość: {wiadomosc}')


    konsument.close()

if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(konsumuj_wiadomosci())
    except KeyboardInterrupt:
        pass
