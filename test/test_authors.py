import requests
from lib.service import Service


service = Service()


def setup_module(module):
    service.start()


def teardown_module(module):
    service.stop()


def test_add_authors():
    result = requests.post("http://127.0.0.1:8000/v1/authors", json={"name": "Arthur C. Clarke"})
    assert result.ok

    result = requests.post("http://127.0.0.1:8000/v1/authors", json={"name": "Stephen Hawking"})
    assert result.ok

    result = requests.get("http://127.0.0.1:8000/v1/authors")
    assert result.json() == {"authors": [{"id": 1, "name": "Arthur C. Clarke"}, {"id": 2, "name": "Stephen Hawking"}]}
