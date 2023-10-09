from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from telegram_bot.models import User


def get_handler():
    def handler(update: Update, context: CallbackContext) -> None:
        id = update.effective_user.id
        try:
            user = User.objects.get(telegram_id=id)
        except User.DoesNotExist:
            user = User(telegram_id=id)
            user.save()

        context.bot.send_message(
            chat_id=update.effective_chat.id, text="$start_message"
        )

    return CommandHandler('start', handler)
