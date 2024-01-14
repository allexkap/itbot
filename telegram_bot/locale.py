import logging

from django.db import models

from telegram_bot.models import User

logger = logging.getLogger('telegram')


class String(models.Model):
    string_id = models.CharField(primary_key=True, max_length=32, db_index=True)
    lang_ru = models.TextField()
    lang_en = models.TextField()


def get_text(string_id: str, user: User) -> str:
    try:
        return getattr(String.objects.get(string_id=string_id), f'lang_{user.language}')

    except String.DoesNotExist:
        raise String.DoesNotExist(
            f'user_id={user.telegram_id}; '
            f'Unknown string id="{string_id}" in locale="{user.language}"'
        )

    except AttributeError:
        logger.error(f'user_id={user.telegram_id}; Unknown locale="{user.language}"')
        logger.info(f'user_id={user.telegram_id}; Override user language with "ru"')
        user.language = 'ru'
        user.save()
        return get_text(string_id, user)
