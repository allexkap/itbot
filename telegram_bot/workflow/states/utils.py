from telegram import Update
from telegram.ext import CallbackContext


def parse_cmd(msg: str):
    return msg[1:].partition(' ')[::2] if msg.startswith('/') else ('', msg)


def parse_commands(states):
    def deco(fun):
        def inner(update: Update, context: CallbackContext):
            cmd, _ = parse_cmd(update.effective_message.text)
            for command in states:
                if cmd == command:
                    return states[cmd]

            return fun(update, context)

        return inner

    return deco
