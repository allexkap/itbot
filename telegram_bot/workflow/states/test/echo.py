from telegram import ParseMode

from telegram_bot.workflow.utils import *


def _help(update: Update, context: CallbackContext, user: User) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_text('state_test_echo:help', user),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


edges = [
    Edge('ready', 'cancel'),
    Edge(_help, 'help'),
]


prepare = send_message_with_reply_keyboard('state_test_echo:text', edges)


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
