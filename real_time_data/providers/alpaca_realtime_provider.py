import os
import json
import websocket
from utils.logging_wrapper import LoggingWrapper
from real_time_data.base_realtime_provider import BaseRealTimeDataProvider

logger = LoggingWrapper(__name__)

class AlpacaRealTimeProvider(BaseRealTimeDataProvider):
    def __init__(self, **config):
        self.api_key = os.getenv(config['api_key_env'])
        self.secret_key = os.getenv(config['secret_key_env'])
        self.url = config['url']
        self.sandbox_url = config.get('sandbox_url', self.url)
        self.feed = config.get('feed', 'iex')
        self.symbol = config['symbol']
        self.use_sandbox = config.get('use_sandbox', False)
        self.ws = None
        logger.info("AlpacaRealTimeProvider initialized")

    def _get_ws_url(self):
        """
        Get the WebSocket URL based on whether sandbox mode is used.
        """
        if self.use_sandbox:
            return self.sandbox_url.format(feed=self.feed)
        return self.url.format(feed=self.feed)

    def connect(self):
        """
        Connect to the WebSocket API.
        """
        try:
            ws_url = self._get_ws_url()
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            self.ws.run_forever()
        except Exception as e:
            logger.error(f"Error connecting to WebSocket: {e}")
            raise

    def subscribe(self, symbol):
        """
        Subscribe to the specified symbol.
        """
        try:
            subscribe_message = {
                "action": "subscribe",
                "bars": [symbol]
            }
            self.ws.send(json.dumps(subscribe_message))
        except Exception as e:
            logger.error(f"Error subscribing to {symbol}: {e}")
            raise

    def on_message(self, ws, message):
        """
        Handle incoming messages.
        """
        try:
            logger.info(message)
            message_data = json.loads(message)
            if isinstance(message_data, list):
                for msg in message_data:
                    self.process_message(msg)
            else:
                self.process_message(message_data)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def process_message(self, message):
        """
        Process a single message.
        """
        try:
            logger.info(f"Processing message: {message}")
            if message.get('T') == 'b':
                logger.info(f"Bar data: {message}")
        except Exception as e:
            logger.error(f"Error processing individual message: {e}")

    def on_error(self, ws, error):
        """
        Handle errors.
        """
        logger.error(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """
        Handle WebSocket closing.
        """
        logger.info(f"WebSocket closed with status code {close_status_code} and message: {close_msg}")

    def on_open(self, ws):
        """
        Handle WebSocket opening.
        """
        try:
            logger.info("WebSocket opened")
            auth_message = {
                "action": "auth",
                "key": self.api_key,
                "secret": self.secret_key
            }
            ws.send(json.dumps(auth_message))
        except Exception as e:
            logger.error(f"Error during WebSocket on_open: {e}")
            raise

    def disconnect(self):
        """
        Disconnect the WebSocket.
        """
        if self.ws:
            self.ws.close()
