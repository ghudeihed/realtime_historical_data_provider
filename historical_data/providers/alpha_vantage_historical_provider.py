import os
import requests
from datetime import datetime, timedelta
from historical_data.base_historical_provider import BaseHistoricalDataProvider
from utils.date_utils import DateUtils
from utils.logging_wrapper import LoggingWrapper

logger = LoggingWrapper(__name__)

class AlphaVantageHistoricalProvider(BaseHistoricalDataProvider):
    def __init__(self, **config):
        self.api_key = os.getenv(config['api_key_env'])
        self.symbol = config['symbol']
        self.function = config['function']
        self.interval = config.get('interval')  # Correctly access interval
        self.outputsize = config['outputsize']
        self.url = config['url']
        logger.info("AlphaVantageHistoricalProvider initialized with config: %s", config)

    def is_market_open(self):
        """
        Check if the market is currently open.
        """
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': self.symbol,
                'interval': self.interval,
                'apikey': self.api_key
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info("Fetched market status")
            return {"is_open": 'Time Series' in data}
        except requests.RequestException as e:
            logger.error(f"Error checking market status: {e.response.text}")
            return {"is_open": False}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"is_open": False}

    def get_historical_data(self, start=None, end=None):
        """
        Fetch historical data for the given symbol.
        """
        try:
            start, end = DateUtils.validate_dates(start, end)
            start_str = start.strftime('%Y-%m-%d')
            end_str = end.strftime('%Y-%m-%d')

            params = {
                'function': self.function,
                'symbol': self.symbol,
                'interval': self.interval,
                'outputsize': self.outputsize,
                'apikey': self.api_key
            }

            logger.debug(f"Fetching data for {self.symbol} from {start_str} to {end_str}")
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'Time Series' in data:
                logger.info(f"Fetched historical data for {self.symbol}")
                return data[f'Time Series ({self.interval})']
            else:
                logger.error(f"Error fetching historical data: {data}")
                raise Exception(f"Alpha Vantage API error: {data}")

        except requests.RequestException as e:
            logger.error(f"Error fetching historical data: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
