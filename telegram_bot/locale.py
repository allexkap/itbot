import logging

from django.db import models

from telegram_bot.models import User


class String(models.Model):
    string_id = models.CharField(primary_key=True, max_length=32, db_index=True)
    lang_ru = models.TextField()
    lang_en = models.TextField()


def get_text(string_id: str, lang: str | User) -> str | None:
    if isinstance(lang, User):
        lang = lang.language
    try:
        return getattr(String.objects.get(string_id=string_id), f'lang_{lang}')
    except String.DoesNotExist:
        logging.error(f'Unknown string id = "{string_id}"')
    except AttributeError:
        logging.error(f'Unknown locale = "{lang}"')
    return None
