from time import sleep
from requests import get, Response

hostname: str = "http://ratelimiting.luxas.xyz:9001/"


def test_exceed():
    for _ in range(5):
        resp: Response = get(hostname)
        assert resp.status_code == 200
    resp: Response = get(hostname)
    assert resp.status_code == 429


def test_wait():
    for _ in range(5):
        resp: Response = get(hostname)
        assert resp.status_code == 200
    sleep(10)
    for _ in range(5):
        resp: Response = get(hostname)
        assert resp.status_code == 200
