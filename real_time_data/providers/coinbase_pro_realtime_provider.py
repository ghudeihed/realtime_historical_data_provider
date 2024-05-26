import websocket
import json
from utils.logging_wrapper import LoggingWrapper
from real_time_data.base_realtime_provider import BaseRealTimeDataProvider

logger = LoggingWrapper(__name__)

class CoinbaseProRealTimeProvider(BaseRealTimeDataProvider):
    def __init__(self, **config):
        self.url = config.get('url')
        self.symbol = config.get('symbol')
        self.api_key_env = config.get('api_key_env')
        self.secret_key_env = config.get('secret_key_env')
        self.use_sandbox = config.get('use_sandbox', False)
        self.ws = None
        logger.info("CoinbaseProRealTimeProvider initialized with config: %s", config)

    def on_message(self, ws, message):
        data = json.loads(message)
        logger.info(f"Received message: {data}")

    def on_error(self, ws, error):
        logger.error(f"Error: {error}")

    def on_close(self, ws):
        logger.info("Connection closed")

    def on_open(self, ws):
        logger.info("Connection opened")
        self.subscribe(ws)

    def subscribe(self, ws):
        subscribe_message = json.dumps({
            "type": "subscribe",
            "channels": [{"name": "ticker", "product_ids": [self.symbol]}]
        })
        ws.send(subscribe_message)

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        self.ws.run_forever()
