from ib_insync import IB, util
import os
from datetime import datetime, timedelta
from utils.date_utils import DateUtils  # Import the DateUtils class
from historical_data.base_historical_provider import BaseHistoricalDataProvider
from utils.logging_wrapper import LoggingWrapper

logger = LoggingWrapper(__name__)

class InteractiveBrokersHistoricalProvider(BaseHistoricalDataProvider):
    def __init__(self, **config):
        self.host = config['host']
        self.port = config['port']
        self.client_id = config['client_id']
        self.symbol = config['symbol']
        self.duration = config['duration']
        self.bar_size = config['bar_size']
        self.ib = IB()
        self.ib.connect(self.host, self.port, clientId=self.client_id)
        logger.info("InteractiveBrokersHistoricalProvider initialized with config: %s", config)

    def is_market_open(self):
        """
        Check if the market is currently open. Placeholder implementation.
        """
        # Placeholder implementation
        return {"is_open": True}

    def get_historical_data(self, start=None, end=None):
        """
        Fetch historical data for the given symbol.
        """
        try:
            start, end = DateUtils.validate_dates(start, end)

            contract = util.formSymbol(self.symbol)
            self.ib.qualifyContracts(contract)

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
            logger.error(f"Error fetching historical data: {e}")
            raise
