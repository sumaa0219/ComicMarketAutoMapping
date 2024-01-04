import json
import requests
import time

url = ["https://webcatalog-free.circle.ms/Map/GetMapping2?day=Day1&hall=e123", "https://webcatalog-free.circle.ms/Map/GetMapping2?day=Day1&hall=e456",
       "https://webcatalog-free.circle.ms/Map/GetMapping2?day=Day1&hall=w12",
       "https://webcatalog-free.circle.ms/Map/GetMapping2?day=Day1&hall=e7",
       "https://webcatalog-free.circle.ms/Map/GetMapping2?day=Day2&hall=e123", "https://webcatalog-free.circle.ms/Map/GetMapping2?day=Day2&hall=e456",
       "https://webcatalog-free.circle.ms/Map/GetMapping2?day=Day2&hall=w12",
       "https://webcatalog-free.circle.ms/Map/GetMapping2?day=Day2&hall=e7"]  # ここにリクエストを送りたいURLを入力

for x in url:
    response = requests.get(x)
    print("Status code:", response.status_code)
    time.sleep(1)


def webCircleInfo(day, place, priority):
    pass
