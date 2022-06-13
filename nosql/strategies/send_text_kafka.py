import asyncio
import json

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

from .send_text import SendText
from nosql.exceptions import NoSuchVariableException


class SendTextKafka(SendText):

    def __init__(self, conn_str: str, eventhub_name: str):
        if conn_str is None or eventhub_name is None:
            raise NoSuchVariableException
        self.producer = EventHubProducerClient.from_connection_string(
            conn_str=conn_str,
            eventhub_name=eventhub_name
        )

    async def send_text(self, text_list: list):
        async with self.producer:
            coros = []
            for dict_obj in text_list:
                text = json.dumps(dict_obj)
                print(text)
                coros.append(self.producer.send_event(EventData(text)))
            await asyncio.gather(*coros)


