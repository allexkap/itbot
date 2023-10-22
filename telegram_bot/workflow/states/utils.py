from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext


def parse_cmd(msg: str):
    return msg[1:].partition(' ')[::2] if msg.startswith('/') else ('', msg)


def parse_commands(edges):
    def inner(fun):
        def func(update: Update, context: CallbackContext) -> None | str:
            cmd, _ = parse_cmd(update.effective_message.text)
            for command in edges:
                if cmd == command:
                    obj = edges[cmd]  # a?
                    return obj(update, context) if callable(obj) else obj

            return fun(update, context)

        return func

    return inner


def get_markup(edges):
    keyboard = (('/' + command,) for command in edges)
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Ваш выбор?",
    )
