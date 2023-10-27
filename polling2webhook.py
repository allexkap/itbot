import json
import os
from argparse import ArgumentParser

import requests

parser = ArgumentParser()
parser.add_argument('-a', '--address', default='localhost')
parser.add_argument('-p', '--port', default='8000')
parser.add_argument('-s', '--https', action='store_true')
parser.add_argument('-t', '--timeout', default='60')
parser.add_argument('-w', '--webhook', default='telegram_bot/webhook/')
args = parser.parse_args()


url_tg = 'https://api.telegram.org/bot{}/getupdates'.format(
    os.getenv('TELEGRAM_BOT_TOKEN')
)
url_wh = '{}://{}:{}/{}'.format(
    'https' if args.https else 'http',
    args.address,
    args.port,
    args.webhook,
)

params = {
    'offset': 0,
    'limit': 1,
    'timeout': args.timeout,
}


while True:
    response = requests.get(url_tg, json=params)
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
