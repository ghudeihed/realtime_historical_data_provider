from abc import ABC, abstractmethod

class BaseRealTimeDataProvider(ABC):
    @abstractmethod
    def on_message(self, ws, message):
        pass

    @abstractmethod
    def on_error(self, ws, error):
        pass

    @abstractmethod
    def on_close(self, ws):
        pass

    @abstractmethod
    def on_open(self, ws):
        pass

    @abstractmethod
    def subscribe(self, ws):
        pass

    @abstractmethod
    def connect(self):
        pass
