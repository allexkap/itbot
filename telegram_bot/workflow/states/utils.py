from dataclasses import dataclass

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext


@dataclass
class Edge:
    next_state: str | callable
    cmd: str
    text: str = ''

    def __eq__(self, rhs: str) -> bool:
        return (
            rhs[0] == '/'
            and rhs[1:].partition(' ')[0] == self.cmd
            or self.text
            and rhs == self.text
        )


def parse_cmd(msg: str) -> tuple[str]:
    return msg[1:].partition(' ')[::2] if msg.startswith('/') else ('', msg)


def parse_commands(edges: list[Edge]) -> callable:
    def inner(fun: callable) -> callable:
        def func(update: Update, context: CallbackContext) -> None | str:
            try:
                pos = edges.index(update.effective_message.text)
                obj = edges[pos].next_state
                return obj(update, context) if callable(obj) else obj
            except ValueError:
                pass
            try:
                return fun(update, context)
            except Exception as ex:
                print(ex)  # todo logging
                return None

        return func

    return inner


def get_markup(edges: list[Edge] = [], params: dict = {}) -> ReplyKeyboardMarkup:
    kwargs = {
        'resize_keyboard': True,
        'one_time_keyboard': False,
        'input_field_placeholder': 'Твой выбор?',
    }
    kwargs.update(params)
    keyboard = ((edge.text,) if edge.text else ('/' + edge.cmd,) for edge in edges)
    return ReplyKeyboardMarkup(keyboard, **kwargs)
