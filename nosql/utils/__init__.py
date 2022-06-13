import requests


def read_from_api(url: str):
    r = requests.get(url)
    return r.json()

