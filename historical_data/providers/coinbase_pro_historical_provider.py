import requests
import os
from datetime import datetime, timedelta, time
from utils.date_utils import DateTimeUtils, DateUtils  # Import the DateUtils class
from historical_data.base_historical_provider import BaseHistoricalDataProvider
from utils.logging_wrapper import LoggingWrapper

logger = LoggingWrapper(__name__)

class CoinbaseProHistoricalProvider(BaseHistoricalDataProvider):
    SUPPORTED_GRANULARITIES = {60, 300, 900, 3600, 21600, 86400}

    def __init__(self, **config):
        self.api_key = os.getenv(config['api_key_env'])
        self.secret_key = os.getenv(config['secret_key_env'])
        self.symbol = config['symbol']
        self.granularity = config['granularity']
        if self.granularity not in self.SUPPORTED_GRANULARITIES:
            raise ValueError(f"Unsupported granularity: {self.granularity}. Supported values are {self.SUPPORTED_GRANULARITIES}.")
        self.url = config['url']
        self.use_sandbox = config.get('use_sandbox', False)
        logger.info("CoinbaseProHistoricalProvider initialized with config: %s", config)

    def is_market_open(self):
        """
        Check if the market is currently open. Placeholder implementation.
        """
        try:
            response = requests.get(f"{self.url}/time")
            response.raise_for_status()
            server_time = response.json()['iso']
            server_time = datetime.fromisoformat(server_time.replace('Z', '+00:00'))

            # Define typical market hours (e.g., 9:30 AM to 4:00 PM EST)
            market_open_time = time(9, 30)
            market_close_time = time(16, 0)

            # Check if the current time is within market hours
            is_open = market_open_time <= server_time.time() <= market_close_time
            return {"is_open": is_open}
        except requests.RequestException as e:
            logger.error(f"Error checking market status: {e}")
            return {"is_open": False}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"is_open": False}

    def get_historical_data(self, start=None, end=None):
        """
        Fetch historical data for the given symbol.
        """
        try:
            start, end = DateUtils.validate_dates(start, end)  # Use the validate_dates method from DateUtils

            start_str = DateTimeUtils.to_rfc3339(start)
            end_str = DateTimeUtils.to_rfc3339(end)

            url_path = f"/products/{self.symbol}/candles"
            params = {
                'start': start_str,
                'end': end_str,
                'granularity': self.granularity
            }

            # Generate the required headers
            headers = {
                'CB-ACCESS-KEY': self.api_key,
                'CB-ACCESS-SIGN': self.secret_key,
                'CB-ACCESS-TIMESTAMP': str(int(datetime.utcnow().timestamp())),
            }

            response = requests.get(f"{self.url}{url_path}", headers=headers, params=params)
            response.raise_for_status()
            logger.info(f"Fetched historical data for {self.symbol}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching historical data: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
