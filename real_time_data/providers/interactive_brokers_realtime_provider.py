from ib_insync import IB, Contract, util
import os
from ..base_realtime_provider import BaseRealTimeDataProvider
from utils.logging_wrapper import LoggingWrapper

logger = LoggingWrapper(__name__)

class InteractiveBrokersRealTimeProvider(BaseRealTimeDataProvider):
    def __init__(self, **config):
        required_keys = ['host', 'port', 'client_id', 'symbol']
        if not all(key in config for key in required_keys):
            logger.error("Initialization failed due to missing configuration parameters.")
            raise ValueError("Missing configuration parameters.")
        self.host = config['host']
        self.port = config['port']
        self.client_id = config['client_id']
        self.symbol = config['symbol']
        self.ib = IB()
        if not self.ib.connect(self.host, self.port, clientId=self.client_id):
            logger.error("Failed to connect to Interactive Brokers TWS API.")
            raise ConnectionError("Could not connect to Interactive Brokers TWS API.")
        logger.info("InteractiveBrokersRealTimeProvider initialized with config: %s", config)

    def connect(self):
        """
        Connect to the IB TWS or Gateway.
        """
        try:
            if not self.ib.isConnected():
                self.ib.connect(self.host, self.port, clientId=self.client_id)
            logger.info("Connected to IB")
        except Exception as e:
            logger.error(f"Error connecting to IB: {e}")
            raise

    def subscribe(self, symbol):
        """
        Subscribe to the specified symbol.
        """
        try:
            contract = Contract(symbol=self.symbol, secType='STK', exchange='SMART', currency='USD')
            self.ib.qualifyContracts(contract)
            self.ib.reqMktData(contract, '', False, False)
            logger.info(f"Subscribed to {symbol}")
        except Exception as e:
            logger.error(f"Error subscribing to {symbol}: {e}")
            raise

    def on_message(self, msg):
        """
        Handle incoming messages.
        """
        try:
            logger.info(msg)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def on_error(self, error):
        """
        Handle errors.
        """
        logger.error(f"Error: {error}")

    def on_close(self):
        """
        Handle connection closing.
        """
        logger.info("Connection closed")

    def on_open(self):
        """
        Handle connection opening.
        """
        try:
            self.subscribe(self.symbol)
        except Exception as e:
            logger.error(f"Error during connection on_open: {e}")
            raise