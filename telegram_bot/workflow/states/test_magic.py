import re

from telegram import ParseMode

from .utils import *

edges = [
    Edge('ready', 'cancel'),
]


def prepare(update: Update, context: CallbackContext, user: User) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Напиши любое сообщение",
        reply_markup=get_markup(edges),
    )


@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> None | str:
    text = update.message.text
    text = re.sub('\.', '', text)
    text = re.sub(' ', 'ㅤ', text)
    text = re.sub('[^ㅤ\n]', '<span class="tg-spoiler">ㅤ</span>', text)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )
    return 'ready'
