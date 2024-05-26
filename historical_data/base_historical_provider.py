from abc import ABC, abstractmethod

class BaseHistoricalDataProvider(ABC):
    @abstractmethod
    def get_historical_data(self, symbol, start=None, end=None, timeframe='1Min'):
        """
        Fetch historical data for the given symbol.
        """
        pass
