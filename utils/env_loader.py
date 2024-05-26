from dotenv import load_dotenv
import os
from utils.logging_wrapper import LoggingWrapper

logger = LoggingWrapper(__name__)

class EnvLoader:
    @staticmethod
    def load_env(file_path='.env'):
        """
        Load environment variables from a .env file.
        """
        try:
            load_dotenv(file_path)
            logger.info(f"Environment variables loaded from {file_path}")
        except Exception as e:
            logger.error(f"Error loading environment variables from {file_path}: {e}")
            raise

    @staticmethod
    def get_env_variable(name, default=None):
        """
        Get the value of an environment variable.
        """
        try:
            value = os.getenv(name, default)
            if value is None:
                logger.warning(f"Environment variable {name} not found, using default value: {default}")
            return value
        except Exception as e:
            logger.error(f"Error getting environment variable {name}: {e}")
            raise
