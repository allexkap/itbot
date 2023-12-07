import yaml
from django.core.management.base import BaseCommand

from itbot.settings import BASE_DIR
from telegram_bot.locale import String


class Command(BaseCommand):
    help = 'Reload locales'

    def handle(self, *args, **kwargs):
        with open(BASE_DIR / 'telegram_bot' / 'locale.yaml') as file:
            data = yaml.load(file.read(), Loader=yaml.Loader)
        for div in data:
            for title in data[div]:
                String(f'{div}:{title}', **data[div][title]).save()
