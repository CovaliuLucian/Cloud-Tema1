import random
import threading

from config import Config
import requests

PORT = Config().data["port"]
uri = "http://127.0.0.1:" + str(PORT)
lang = ['ro', 'ru', 'en', 'fr', 'it']

barrier = threading.Barrier(20)


def random_word():
    empty = random.choice([True, False])
    if empty:
        return ""
    return "testing"


def random_lang():
    return random.choice(lang)


def test_translation():
    barrier.wait()
    data = {
        "text": random_word(),
        "lang": random_lang()
    }
    r = requests.post(uri + "/translate", json=data)


def test_random():
    barrier.wait()
    r = requests.get(uri + "/random")


def test_se():
    barrier.wait()
    r = requests.get(uri + "/se")


def thread_it(n, f):
    t = []
    for i in range(0, n):
        t += [threading.Thread(target=f)]
    for _th in t: _th.start()
    for _th in t: _th.join()


if __name__ == '__main__':
    # thread_it(100, test_translation)
    # thread_it(100, test_se)
    thread_it(100, test_random)
