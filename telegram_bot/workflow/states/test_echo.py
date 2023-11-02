from telegram import ParseMode

from .utils import *


def _help(update: Update, context: CallbackContext, user: User) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='`//cancel` to suppress command',
        parse_mode=ParseMode.MARKDOWN_V2,
    )


edges = [
    Edge('ready', 'cancel'),
    Edge(_help, 'help'),
]


prepare = send_message_with_reply_keyboard('Напиши любое сообщение', edges)


@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> str | None:
    raw = update.message.text_html
    if raw.startswith('//'):
        raw = raw[1:]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=raw,
        parse_mode=ParseMode.HTML,
    )
    return 'ready'
