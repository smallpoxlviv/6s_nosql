import json
import time

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

from .send_text import SendText


class SendTextKafka(SendText):

    def __init__(self, conn_str: str, eventhub_name: str):
        if conn_str is None or eventhub_name is None:
            raise Exception('No conn_str or eventhub_name')
        self.producer = EventHubProducerClient.from_connection_string(
            conn_str=conn_str,
            eventhub_name=eventhub_name
        )

    async def send_text(self, text_list: list):
        start_time = time.time()
        async with self.producer:
            event_data_batch = await self.producer.create_batch()
            for dict_obj in text_list:
                text = json.dumps(dict_obj)
                event_data = EventData(text)
                try:
                    event_data_batch.add(event_data)
                except ValueError:
                    await self.producer.send_batch(event_data_batch)
                    event_data_batch = await self.producer.create_batch()
                    event_data_batch.add(event_data)
            if len(event_data_batch) > 0:
                await self.producer.send_batch(event_data_batch)

        print(f"Send messages in {time.time() - start_time} seconds.")
