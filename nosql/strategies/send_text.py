from abc import ABC, abstractmethod


class SendText(ABC):

    @abstractmethod
    def send_text(self, text: str):
        pass
