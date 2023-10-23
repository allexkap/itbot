from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot.models import User

from . import states


def workflow_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    try:
        user = User.objects.get(telegram_id=user_id)
    except User.DoesNotExist:
        user = User(telegram_id=user_id)
        user.workflow_state = 'reset'
        user.save()

    try:
        next_state = states[user.workflow_state].process(update, context)
    except KeyError:
        next_state = 'ready'

    result = states[next_state].prepare(update, context)
    if result:
        return

    user.workflow_state = next_state
    user.save()
