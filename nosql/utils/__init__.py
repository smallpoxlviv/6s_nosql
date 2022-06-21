import requests


def read_from_api(url: str):
    r = requests.get(url)
    return r.json()


def file_name_from_url(url: str):
    return url.split('/')[-1]
