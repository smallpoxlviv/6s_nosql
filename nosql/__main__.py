import os
import time

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks

from redis_connector import RedisConnector
from strategies import Strategy, SendTextConsole, SendTextKafka, SendTextFile
from utils import read_from_api, file_name_from_url

app = FastAPI()

load_dotenv()
CONN_STR = os.getenv('CONN_STR')
EVENTHUB_NAME = os.getenv('EVENTHUB_NAME')
R_HOST = os.getenv('R_HOST')
R_PORT = os.getenv('R_PORT')
R_ACCESS_KEY = os.getenv('R_ACCESS_KEY')


send_text_kafka = SendTextKafka(conn_str=CONN_STR, eventhub_name=EVENTHUB_NAME)
send_text_console = SendTextConsole()
send_text_file = SendTextFile()
redis = RedisConnector(access_key=R_ACCESS_KEY, host=R_HOST, port=int(R_PORT))


@app.get("/")
async def root():
    return 'ok'


@app.get("/api")
async def process(json_url: str, background_tasks: BackgroundTasks, strategy: str = Strategy.CONSOLE):
    completed = redis.hget(json_url, 'completed')
    if completed:
        return f"You tried to process file {json_url} several times"
    else:
        background_tasks.add_task(main, json_url, strategy)
        redis.hset(name=json_url, key='name', value=file_name_from_url(json_url))
        redis.hset(name=json_url, key='start_time', value=time.time())
        return f"Processing started with strategy: {strategy}. File path: '{json_url}'"


@app.get("/del_redis")
async def del_from_redis(json_url: str):
    return f'url: {json_url}, response: {redis.hdel(json_url)}'


@app.get("/redis")
async def get_from_redis(json_url: str):
    return {
        'name': redis.hget(json_url, 'name'),
        'start_time': redis.hget(json_url, 'start_time'),
        'completed': redis.hget(json_url, 'completed')
    }


async def main(file_url: str, strategy: Strategy):
    text = read_from_api(file_url)
    if strategy == Strategy.CONSOLE:
        send_text_console.send_text(text)
    elif strategy == Strategy.KAFKA:
        await send_text_kafka.send_text(text)
    elif strategy == Strategy.FILE:
        send_text_file.send_text(file_name_from_url(file_url), text)
    redis.hset(name=file_url, key='completed', value='true')


if __name__ == '__main__':
    uvicorn.run(app, port=8081, host='0.0.0.0')
