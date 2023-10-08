from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="yeah")

updater = Updater(token=settings.TELEGRAM_BOT_TOKEN, use_context=True)

dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        json_string = request.body.decode('UTF-8')
        update = Update.de_json(json.loads(json_string), updater.bot)
        dispatcher.process_update(update)

    return JsonResponse({'status':'ok'})
