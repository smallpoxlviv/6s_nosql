from enum import Enum
from .send_text import SendText
from .send_text_kafka import SendTextKafka
from .send_text_console import SendTextConsole
from .send_text_file import SendTextFile


class Strategy(str, Enum):
    KAFKA = 'kafka'
    CONSOLE = 'console'
    FILE = 'file'