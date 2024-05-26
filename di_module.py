from injector import Module, Binder, singleton
from real_time_data.base_realtime_provider import BaseRealTimeDataProvider
from real_time_data.providers.alpaca_realtime_provider import AlpacaRealTimeProvider
from real_time_data.providers.alpha_vantage_realtime_provider import AlphaVantageRealTimeProvider
from real_time_data.providers.interactive_brokers_realtime_provider import InteractiveBrokersRealTimeProvider
from real_time_data.providers.coinbase_pro_realtime_provider import CoinbaseProRealTimeProvider
from historical_data.base_historical_provider import BaseHistoricalDataProvider
from historical_data.providers.alpaca_historical_provider import AlpacaHistoricalProvider
from historical_data.providers.alpha_vantage_historical_provider import AlphaVantageHistoricalProvider
from historical_data.providers.interactive_brokers_historical_provider import InteractiveBrokersHistoricalProvider
from historical_data.providers.coinbase_pro_historical_provider import CoinbaseProHistoricalProvider
from utils.logging_wrapper import LoggingWrapper

logger = LoggingWrapper(__name__)

class Config:
    def __init__(self, provider, realtime_config=None, historical_config=None):
        self.provider = provider
        self.realtime_config = realtime_config
        self.historical_config = historical_config

class RealTimeDataProviderModule(Module):
    def __init__(self, config):
        self.config = config

    def configure(self, binder: Binder):
        provider_map = {
            'alpaca': AlpacaRealTimeProvider,
            'alpha_vantage': AlphaVantageRealTimeProvider,
            'interactive_brokers': InteractiveBrokersRealTimeProvider,
            'coinbase_pro': CoinbaseProRealTimeProvider
        }
        provider_class = provider_map.get(self.config.provider)
        if provider_class:
            binder.bind(BaseRealTimeDataProvider, to=provider_class(**self.config.realtime_config), scope=singleton)
            logger.info(f"Configured {self.config.provider} provider for real-time data")
        else:
            raise ValueError(f"Unsupported real-time provider type: {self.config.provider}")

class HistoricalDataProviderModule(Module):
    def __init__(self, config):
        self.config = config

    def configure(self, binder: Binder):
        provider_map = {
            'alpaca': AlpacaHistoricalProvider,
            'alpha_vantage': AlphaVantageHistoricalProvider,
            'interactive_brokers': InteractiveBrokersHistoricalProvider,
            'coinbase_pro': CoinbaseProHistoricalProvider
        }
        provider_class = provider_map.get(self.config.provider)
        if provider_class:
            binder.bind(BaseHistoricalDataProvider, to=provider_class(**self.config.historical_config), scope=singleton)
            logger.info(f"Configured {self.config.provider} provider for historical data")
        else:
            raise ValueError(f"Unsupported historical provider type: {self.config.provider}")
