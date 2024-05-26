from ib_insync import IB, util
import os
from ..base_realtime_provider import BaseRealTimeDataProvider
from utils.logging_wrapper import LoggingWrapper

logger = LoggingWrapper(__name__)

class InteractiveBrokersRealTimeProvider(BaseRealTimeDataProvider):
    def __init__(self, **config):
        self.host = config.get('host')
        self.port = config.get('port')
        self.client_id = config.get('client_id')
        self.symbol = config.get('symbol')
        self.ib = IB()
        logger.info("IBProvider initialized")

    def connect(self):
        """
        Connect to the IB TWS or Gateway.
        """
        try:
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
            contract = util.formSymbol(symbol)
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

    def process_message(self, msg):
        """
        Process a single message.
        """
        try:
            logger.info(msg)
        except Exception as e:
            logger.error(f"Error processing individual message: {e}")

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
