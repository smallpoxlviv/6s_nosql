import json

from .send_text import SendText


class SendTextConsole(SendText):

    def send_text(self, text_list: list):
        for text in text_list:
            print(json.dumps(text))
