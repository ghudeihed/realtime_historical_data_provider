# Real-Time and Historical Data Provider

## Overview

This project provides a unified interface to access both real-time and historical financial market data from various providers, including Alpaca, Coinbase Pro, and Interactive Brokers. The goal is to simplify the process of switching between different data providers by using a common configuration and dependency injection mechanism.

## Features

- **Real-Time Data**: Connects to real-time data streams from supported providers.
- **Historical Data**: Fetches historical data for specified time intervals.
- **Dependency Injection**: Utilizes dependency injection for flexible and testable code.
- **Configuration Driven**: Easily switch providers by updating configuration files.
- **Environment Management**: Securely manages API keys and other secrets.

## Project Structure

```
project_root/
│
├── config/
│   └── config.json
│
├── historical_data/
│   ├── __init__.py
│   ├── base_historical_provider.py
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── alpaca_historical_provider.py
│   │   ├── interactive_brokers_historical_provider.py
│   │   ├── coinbase_pro_historical_provider.py
│
├── real_time_data/
│   ├── __init__.py
│   ├── base_realtime_provider.py
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── alpaca_realtime_provider.py
│   │   ├── coinbase_pro_realtime_provider.py
│   │   ├── interactive_brokers_realtime_provider.py
│
├── utils/
│   └── env_loader.py
│   └── logging_wrapper.py
│   └── date_utils.py
│
├── di_module.py
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── .env
```

## Setup

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)

### Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/real_time_data_provider.git
   cd real_time_data_provider
   ```

2. **Create and activate a virtual environment**:
   ```sh
   python3.9 -m venv findata
   source findata/bin/activate  # On Windows use `findata\Scripts\activate`
   ```
   or 
   ```sh
    conda create -n findata python=3.9.19 -y
    conda activate findata
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Export virtual envirment**:
   ```sh
   conda env export -n findata > envirment.yml
   ```

5. **Set up environment variables**:
   Create a `.env` file in the project root and add your API keys and secrets:
   ```env
   PROVIDER_NAME=alpaca  # or 'coinbase_pro', 'interactive_brokers'
   ALPACA_API_KEY=your_alpaca_api_key
   ALPACA_SECRET_KEY=your_alpaca_secret_key
   COINBASE_PRO_API_KEY=your_coinbase_pro_api_key
   COINBASE_PRO_SECRET_KEY=your_coinbase_pro_secret_key
   ```

### Configuration

The configuration file `config/config.json` should contain settings for each provider. Example configuration:

```json
[
    {
        "provider": "interactive_brokers",
        "realtime": {
            "host": "127.0.0.1",
            "port": 7497,
            "client_id": 1,
            "symbol": "AAPL",
            "use_sandbox": true
        },
        "historical": {
            "host": "127.0.0.1",
            "port": 7497,
            "client_id": 1,
            "symbol": "AAPL",
            "duration": "1 D",
            "bar_size": "1 min",
            "use_sandbox": true
        }
    },
    {
        "provider": "alpaca",
        "realtime": {
            "url": "wss://stream.data.alpaca.markets/v2/{feed}",
            "sandbox_url": "wss://stream.data.sandbox.alpaca.markets/v2/{feed}",
            "api_key_env": "ALPACA_API_KEY",
            "secret_key_env": "ALPACA_SECRET_KEY",
            "feed": "iex",
            "symbol": "AAPL",
            "use_sandbox": true
        },
        "historical": {
            "api_key_env": "ALPACA_API_KEY",
            "secret_key_env": "ALPACA_SECRET_KEY",
            "symbol": "AAPL",
            "timeframe": "1Min",
            "use_sandbox": true,
            "sandbox_url": "https://paper-api.alpaca.markets",
            "url": "https://api.alpaca.markets",
            "data_url": "https://data.alpaca.markets/v2"
        }
    },
    {
        "provider": "coinbase_pro",
        "realtime": {
            "url": "wss://ws-feed.pro.coinbase.com",
            "symbol": "BTC-USD",
            "use_sandbox": true
        },
        "historical": {
            "api_key_env": "COINBASE_PRO_API_KEY",
            "secret_key_env": "COINBASE_PRO_SECRET_KEY",
            "symbol": "BTC-USD",
            "granularity": 3600,
            "use_sandbox": true,
            "url": "https://api.pro.coinbase.com"
        }
    }
]
```

## Usage

Run the main script with the desired data type (historical or real-time):

```sh
python main.py --data-type realtime
```

or

```sh
python main.py --data-type historical
```

## Modules

### `historical_data`

- **base_historical_provider.py**: Abstract base class for historical data providers.
- **providers/alpaca_historical_provider.py**: Alpaca historical data implementation.
- **providers/coinbase_pro_historical_provider.py**: Coinbase Pro historical data implementation.
- **providers/interactive_brokers_historical_provider.py**: Interactive Brokers historical data implementation.

### `real_time_data`

- **base_realtime_provider.py**: Abstract base class for real-time data providers.
- **providers/alpaca_realtime_provider.py**: Alpaca real-time data implementation.
- **providers/coinbase_pro_realtime_provider.py**: Coinbase Pro real-time data implementation.
- **providers/interactive_brokers_realtime_provider.py**: Interactive Brokers real-time data implementation.

### `utils`

- **env_loader.py**: Loads environment variables from a `.env` file.
- **logging_wrapper.py**: Wrapper around the logging module for simplified logging.
- **date_utils.py**: Utility functions, including date and time handling.

### `di_module.py`

Defines the dependency injection modules for real-time and historical data providers.

### `main.py`

Main script to run the data providers based on user input.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Alpaca](https://alpaca.markets)
- [Coinbase Pro](https://pro.coinbase.com)
- [Interactive Brokers](https://www.interactivebrokers.com)
- [Python](https://www.python.org)
- [WebSocket](https://websockets.readthedocs.io/en/stable/)
- [Requests](https://docs.python-requests.org/en/latest/)