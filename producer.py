import os
import json
import logging
from aiohttp import web
from confluent_kafka import Producer

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Konfiguracja producenta Kafka
konfiguracja_producenta = {
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS', 'localhost:9092')
}
producent = Producer(konfiguracja_producenta)

# Funkcja callback dla dostarczania wiadomości
def callback_dostarczenia(err, msg):
    if err:
        logger.error(f'Nie udało się dostarczyć wiadomości: {err}')
    else:
        logger.info(f'Wiadomość dostarczona do {msg.topic()} [{msg.partition()}]')

async def wyprodukuj_wiadomosc(request):
    dane = await request.json()
    temat = dane.get('topic', 'default_topic')
    wiadomosc = json.dumps(dane.get('message', {}))
    
    producent.produce(temat, wiadomosc.encode('utf-8'), callback=callback_dostarczenia)
    producent.flush()
    
    return web.json_response({'status': 'wiadomość wyprodukowana'}, status=200)

app = web.Application()
app.router.add_post('/produce', wyprodukuj_wiadomosc)

# Dodanie dokumentacji Swagger
from aiohttp_swagger import setup_swagger
setup_swagger(app, swagger_url="/api/doc", title="Producer API", description="API do produkcji wiadomości do Kafki")

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
