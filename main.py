import json
import argparse
from datetime import datetime, timezone
from injector import Injector
from di_module import Config, RealTimeDataProviderModule, HistoricalDataProviderModule
from real_time_data.base_realtime_provider import BaseRealTimeDataProvider
from historical_data.base_historical_provider import BaseHistoricalDataProvider
from utils.env_loader import EnvLoader
from utils.logging_wrapper import LoggingWrapper

logger = LoggingWrapper(__name__)

def load_config(file_path, provider_name):
    """
    Load the configuration for the given provider from the specified JSON file.

    :param file_path: Path to the JSON configuration file.
    :param provider_name: Name of the provider to load the configuration for.
    :return: Configuration dictionary for the specified provider.
    """
    try:
        with open(file_path, 'r') as file:
            configs = json.load(file)
            for config in configs:
                if config['provider'] == provider_name:
                    return config
            raise ValueError(f"No configuration found for provider: {provider_name}")
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise

def get_real_time_data(config):
    """
    Set up and run the real-time data provider.
    
    :param config: Configuration object for the provider.
    """
    try:
        injector = Injector([RealTimeDataProviderModule(config)])
        provider = injector.get(BaseRealTimeDataProvider)
        provider.connect()
    except Exception as e:
        logger.error(f"Error in real-time data provider: {e}")

def get_historical_data(config):
    """
    Set up and run the historical data provider.
    
    :param config: Configuration object for the provider.
    """
    try:
        injector = Injector([HistoricalDataProviderModule(config)])
        historical_provider = injector.get(BaseHistoricalDataProvider)

        # Define the start and end dates
        start_date = datetime(2024, 5, 24, tzinfo=timezone.utc)
        end_date = datetime(2024, 5, 25, tzinfo=timezone.utc)

        # Fetch historical data
        historical_data = historical_provider.get_historical_data(start=start_date, end=end_date)
        logger.info(f"Historical data: {historical_data}")

        print(historical_data)
    except Exception as e:
        logger.error(f"Error in historical data provider: {e}")

def main():
    parser = argparse.ArgumentParser(description="Select data type to fetch (historical or real-time)")
    parser.add_argument('--data-type', type=str, required=True, choices=['historical', 'realtime'], 
                        help="Specify the data type to fetch: 'historical' or 'realtime'")
    args = parser.parse_args()

    try:
        # Load environment variables from .env file
        EnvLoader.load_env('.env')

        # Get the provider name from environment variables
        provider_name = EnvLoader.get_env_variable('PROVIDER_NAME', 'binance')
        logger.info(f"Using provider: {provider_name}")

        # Load the configuration for the specified provider
        config_data = load_config('config/config.json', provider_name)
        config = Config(provider=provider_name, realtime_config=config_data['realtime'], historical_config=config_data['historical'])

        if args.data_type == 'realtime':
            get_real_time_data(config)
        elif args.data_type == 'historical':
            get_historical_data(config)
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
