from collections.abc import Callable
from dataclasses import dataclass

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

from telegram_bot.locale import get_text
from telegram_bot.models import User

WorkflowFunction = Callable[[Update, CallbackContext, User], str | None]


@dataclass
class Edge:
    next_state: str | WorkflowFunction
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


def parse_commands(edges: list[Edge]) -> Callable[[WorkflowFunction], WorkflowFunction]:
    def decorator(fun: WorkflowFunction) -> WorkflowFunction:
        def func(update: Update, context: CallbackContext, user: User) -> str | None:
            try:
                pos = edges.index((update.effective_message.text))
                obj = edges[pos].next_state
                return obj(update, context, user) if callable(obj) else obj
            except ValueError:
                pass
            try:
                return fun(update, context, user)
            except Exception as ex:
                print(ex)  # todo logging
                return None

        return func

    return decorator


def get_reply_markup(
    edges: list[Edge] | None = None, lang: str | User | None = None
) -> ReplyKeyboardMarkup | ReplyKeyboardRemove:
    if edges is None:
        return ReplyKeyboardRemove()
    assert lang  # None lang available only for None edges
    kwargs = {
        'resize_keyboard': True,
        'one_time_keyboard': False,
        'input_field_placeholder': get_text('global:placeholder', lang),
    }
    keyboard = ((edge.text,) if edge.text else ('/' + edge.cmd,) for edge in edges)
    return ReplyKeyboardMarkup(keyboard, **kwargs)


def send_message_with_reply_keyboard(string_id: str, *args, **kwargs):
    assert len(args) <= 1 and 'lang' not in kwargs  # check lang not in params

    def func(update: Update, context: CallbackContext, user: User) -> str | None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_text(string_id, user),
            reply_markup=get_reply_markup(*args, lang=user, **kwargs),
        )

    return func
