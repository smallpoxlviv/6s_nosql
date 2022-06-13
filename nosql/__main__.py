import os

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from dotenv import load_dotenv

from nosql.strategies import SendTextFile
from strategies import Strategy, SendTextConsole, SendTextKafka
from utils import read_from_api

app = FastAPI()

load_dotenv()
CONN_STR = os.getenv('CONN_STR')
EVENTHUB_NAME = os.getenv('EVENTHUB_NAME')
STRATEGY = os.getenv('STRATEGY', default='file')


send_text_kafka = SendTextKafka(conn_str=CONN_STR, eventhub_name=EVENTHUB_NAME)
send_text_console = SendTextConsole()
send_text_file = SendTextFile()


@app.get("/")
async def root():
    return 'ok'


@app.get("/api/")
async def process(json_url: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(main, json_url, STRATEGY)
    return f"Processing started with strategy: {STRATEGY}. File path: '{json_url}'"


async def main(file_url: str, strategy: Strategy):
    text = read_from_api(file_url)
    if strategy == Strategy.CONSOLE:
        send_text_console.send_text(text)
    elif strategy == Strategy.KAFKA:
        await send_text_kafka.send_text(text)
    elif strategy == Strategy.FILE:
        send_text_file.send_text(text)


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='localhost')
