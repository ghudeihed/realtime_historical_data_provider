from ib_insync import IB, Stock, util
import os
from datetime import datetime, timedelta
from utils.date_utils import DateUtils  # Import the DateUtils class
from historical_data.base_historical_provider import BaseHistoricalDataProvider
from utils.logging_wrapper import LoggingWrapper

logger = LoggingWrapper(__name__)

class InteractiveBrokersHistoricalProvider(BaseHistoricalDataProvider):
    def __init__(self, **config):
        required_keys = ['host', 'port', 'client_id', 'symbol', 'duration', 'bar_size']
        if not all(key in config for key in required_keys):
            logger.error("Initialization failed due to missing configuration parameters.")
            raise ValueError("Missing configuration parameters.")
        self.host = config['host']
        self.port = config['port']
        self.client_id = config['client_id']
        self.symbol = config['symbol']
        self.duration = config['duration']
        self.bar_size = config['bar_size']
        self.ib = IB()
        if not self.ib.connect(self.host, self.port, clientId=self.client_id):
            logger.error("Failed to connect to Interactive Brokers TWS API.")
            raise ConnectionError("Could not connect to Interactive Brokers TWS API.")
        logger.info("InteractiveBrokersHistoricalProvider initialized with config: %s", config)

    def is_market_open(self):
        """
        Check if the market is currently open.
        """
        # Real implementation needed here
        now = datetime.now()
        # Assuming market open times for NYSE as an example
        open_time = datetime(now.year, now.month, now.day, 9, 30)  # Market opens at 9:30 AM
        close_time = datetime(now.year, now.month, now.day, 16, 0)  # Market closes at 4:00 PM
        return open_time <= now <= close_time

    def get_historical_data(self, start=None, end=None):
        """
        Fetch historical data for the given symbol between start and end dates.
        """
        try:
            start, end = DateUtils.validate_dates(start, end)
            logger.debug(f"Validated dates - Start: {start}, End: {end}")

            contract = self.create_contract()

            logger.debug(f"Requesting historical data for {self.symbol}")
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime=end,
                durationStr=self.duration,
                barSizeSetting=self.bar_size,
                whatToShow='MIDPOINT',
                useRTH=True
            )

            logger.info(f"Fetched historical data for {self.symbol}")
            return util.df(bars).to_json()
        except Exception as e:
            logger.error(f"Error fetching historical data for {self.symbol}: {e}")
            raise

    def create_contract(self):
        """
        Create a contract object for the symbol.
        """
        return Stock(self.symbol, 'SMART', 'USD')