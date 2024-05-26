import os
import requests
from utils.logging_wrapper import LoggingWrapper
from real_time_data.base_realtime_provider import BaseRealTimeDataProvider

logger = LoggingWrapper(__name__)

class AlphaVantageRealTimeProvider(BaseRealTimeDataProvider):
    def __init__(self, **config):
        self.api_key = os.getenv(config['api_key_env'])
        self.symbol = config['symbol']
        self.function = config['function']
        self.interval = config['interval']
        self.url = config['url']
        logger.info("AlphaVantageRealTimeProvider initialized with config: %s", config)

    def connect(self):
        """
        Fetch real-time data using Alpha Vantage REST API.
        """
        try:
            response = self.get_real_time_data(self.symbol)
            self.process_message(response)
        except Exception as e:
            logger.error(f"Error fetching real-time data: {e}")
            raise

    def get_real_time_data(self, symbol):
        """
        Fetch real-time data from Alpha Vantage.
        """
        try:
            params = {
                "function": self.function,
                "symbol": symbol,
                "interval": self.interval,
                "apikey": self.api_key
            }
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching data from Alpha Vantage: {e}")
            raise

    def process_message(self, message):
        """
        Process the fetched real-time data.
        """
        try:
            logger.info(f"Received data: {message}")
            # Implement your logic to handle the real-time data
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    # Placeholder methods for WebSocket-based abstract methods
    def subscribe(self, symbol):
        logger.info(f"Subscription is not applicable for Alpha Vantage REST API")

    def on_message(self, ws, message):
        logger.info(f"Message handler is not applicable for Alpha Vantage REST API")

    def on_error(self, ws, error):
        logger.error(f"WebSocket error handler is not applicable for Alpha Vantage REST API")

    def on_close(self, ws, close_status_code, close_msg):
        logger.info(f"WebSocket close handler is not applicable for Alpha Vantage REST API")

    def on_open(self, ws):
        logger.info(f"WebSocket open handler is not applicable for Alpha Vantage REST API")

    def disconnect(self):
        logger.info("AlphaVantageRealTimeProvider disconnected")
