import os
import requests
from alpaca_trade_api.rest import REST
from historical_data.base_historical_provider import BaseHistoricalDataProvider
from utils.date_utils import DateUtils
from utils.logging_wrapper import LoggingWrapper

logger = LoggingWrapper(__name__)

class AlpacaHistoricalProvider(BaseHistoricalDataProvider):
    def __init__(self, **config):
        self.api_key = os.getenv(config['api_key_env'])
        self.secret_key = os.getenv(config['secret_key_env'])
        if not self.api_key or not self.secret_key:
            raise ValueError("API key and secret key must be set in environment variables.")
        self.symbol = config['symbol']
        self.timeframe = config['timeframe']
        self.use_sandbox = config.get('use_sandbox', False)
        self.base_url = config['url']
        self.data_url = config['data_url']
        self.api = REST(self.api_key, self.secret_key, base_url=self.base_url)
        logger.info("AlpacaHistoricalProvider initialized with config: %s", config)

    def is_market_open(self):
        """
        Check if the market is currently open.
        """
        try:
            url = f"{self.base_url}/v2/clock"
            headers = {
                'APCA-API-KEY-ID': self.api_key,
                'APCA-API-SECRET-KEY': self.secret_key
            }
            logger.debug(f"Making request to {url} with headers {headers}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.info("Fetched market status")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error checking market status: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def get_historical_data(self, start=None, end=None):
        """
        Fetch historical data for the given symbol.

        :param start: The start date for the data.
        :param end: The end date for the data.
        :return: Historical data in JSON format.
        """
        try:
            start, end = DateUtils.validate_dates(start, end)
            start_str = start.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_str = end.strftime('%Y-%m-%dT%H:%M:%SZ')

            logger.debug(f"Fetching data for {self.symbol} from {start_str} to {end_str}")
            bars = self.api.get_bars(
                self.symbol,
                self.timeframe,
                start=start_str,
                end=end_str
            ).df

            logger.info(f"Fetched historical data for {self.symbol}")
            return bars.to_json()
        except requests.RequestException as e:
            logger.error(f"Error fetching historical data: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
