from telegram import Update
from telegram.ext import CallbackContext


def parse_cmd(msg: str):
    return msg[1:].partition(' ')[::2] if msg.startswith('/') else ('', msg)
