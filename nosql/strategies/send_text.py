from abc import ABC, abstractmethod


class SendText(ABC):

    @abstractmethod
    def send_text(self, *args, **kwargs):
        pass
