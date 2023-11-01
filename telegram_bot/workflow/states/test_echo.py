from telegram import ParseMode

from .utils import *


def _help(update: Update, context: CallbackContext, user: User) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="`//cancel` to suppress command",
        parse_mode=ParseMode.MARKDOWN_V2,
    )


edges = [
    Edge('ready', 'cancel'),
    Edge(_help, 'help'),
]


def prepare(update: Update, context: CallbackContext, user: User) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Напиши любое сообщение",
        reply_markup=get_markup(edges),
    )


@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> None | str:
    raw = update.message.text_html
    if raw.startswith('//'):
        raw = raw[1:]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=raw,
        parse_mode=ParseMode.HTML,
    )
    return 'ready'
