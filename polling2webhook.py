import json
import os

import requests

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

url_tg = 'https://api.telegram.org/bot%s/getupdates'
url_wh = 'http://localhost:8000/telegram_bot/webhook/'

params = {
    'offset': 0,
    'limit': 1,
    'timeout': 60,
}


while True:
    response = requests.get(url_tg % TELEGRAM_BOT_TOKEN, json=params)
    if not response.ok:
        print(response, response.content)
        break

    results = json.loads(response.content)['result']
    if not results:
        continue
    result = results[0]
    print(result)

    params['offset'] = result['update_id'] + 1
    requests.post(url_wh, json=result)
