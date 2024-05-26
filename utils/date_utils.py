import pytz
from datetime import datetime, timedelta
from utils.logging_wrapper import LoggingWrapper

logger = LoggingWrapper(__name__)

class DateUtils:
    @staticmethod
    def validate_dates(start, end):
        """
        Validate and adjust the start and end dates based on the criteria:
        1. Start date and end date should never be in the future.
        2. End date should be greater than start date.
        3. Start date should be less than today's date.
        """
        pst = pytz.timezone('America/Los_Angeles')
        current_time = datetime.now(pytz.utc).astimezone(pst)
        logger = LoggingWrapper(__name__)
        logger.info(f'current_time (PST): {current_time}')

        if end is None or end > current_time:
            end = current_time - timedelta(minutes=1)  # Ensure end time is not in the future
            logger.info(f'end (PST): {end}')
        if start is None or start >= end:
            start = end - timedelta(days=1)
            logger.info(f'start (PST): {start}')
        if start >= current_time:
            start = current_time - timedelta(days=1)
            logger.info(f'adjusted start (PST): {start}')
        return start, end

class DateTimeUtils:
    @staticmethod
    def to_rfc3339(dt):
        """
        Convert a datetime object to RFC3339 format with timezone information.
        """
        try:
            if dt.tzinfo is None:
                return dt.isoformat() + 'Z'
            return dt.isoformat()
        except Exception as e:
            logger.error(f"Error converting datetime to RFC3339: {e}")
            raise