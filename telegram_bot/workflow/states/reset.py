from .utils import *


def prepare(update: Update, context: CallbackContext) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="$reset_message",
    )


def process(update: Update, context: CallbackContext) -> None | str:
    cmd, _ = parse_cmd(update.effective_message.text)
    if cmd == 'start':
        return 'start'
