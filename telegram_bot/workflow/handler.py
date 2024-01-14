from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot.locale import get_text
from telegram_bot.models import User

from . import states
from .utils import logger


def workflow_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    try:
        user = User.objects.get(telegram_id=user_id)
    except User.DoesNotExist:
        logger.info(f'new user "{update.effective_user.name}" with {user_id=}')
        user = User(telegram_id=user_id)
        user.set_workflow_state('disabled')

    try:
        next_state = states[user.workflow_state].process(update, context, user)
        if next_state:
            if states[next_state].prepare(update, context, user):
                next_state = None

    except Exception as ex:
        logger.error(
            f'{user_id=}; '
            f'message="{update.effective_message.text}"; '
            f'state={user.workflow_state}; {ex}'
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=get_text('global:error', user)
        )
        states[next_state:='ready'].prepare(update, context, user)

    finally:
        if not next_state:
            return
        logger.info(
            f'{user_id=}; update workflow state: '
            f'{user.workflow_state} -> {next_state}'
        )
        user.set_workflow_state(next_state)
