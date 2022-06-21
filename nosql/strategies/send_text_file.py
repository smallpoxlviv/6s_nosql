import json

from .send_text import SendText


class SendTextFile(SendText):

    def send_text(self, file_name: str, text_list: list):
        with open(f'../resources/', 'w+') as f:
            for text in text_list:
                f.write(f'{json.dumps(text)}\n')
