import json

import requests
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import MessageHandler, Updater

from telegram_bot.models import User
from telegram_bot.workflow.handler import workflow_handler

updater = Updater(token=settings.TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(None, workflow_handler))


@csrf_exempt
def webhook(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        json_string = request.body.decode('UTF-8')
        update = Update.de_json(json.loads(json_string), updater.bot)
        dispatcher.process_update(update)

    return JsonResponse({'status': 'ok'})


@csrf_exempt
def keycloak(request: HttpRequest) -> HttpResponse:
    try:
        r = requests.post(
            settings.KEYCLOAK_REALM_URL + '/protocol/openid-connect/token',
            data={
                'grant_type': 'authorization_code',
                'client_id': settings.KEYCLOAK_CLIENT_ID,
                'client_secret': settings.KEYCLOAK_CLIENT_SECRET,
                'redirect_uri': settings.KEYCLOAK_REDIRECT_URL,
                'code': request.GET['code'],
            },
        )
        assert r.status_code == 200
        keycloak_response = r.json()
    except KeyError:
        error_description = 'Missing form parameter: code'
    except AssertionError:
        error_description = 'Incorrect form parameter: code'
    else:
        try:
            user = User.objects.get(telegram_id=request.GET['state'])
            assert user.id_token == 'waiting'
        except KeyError:
            error_description = 'Missing form parameter: state'
        except (User.DoesNotExist, AssertionError):
            error_description = 'Incorrect form parameter: state'
        else:
            user.access_token = keycloak_response['access_token']
            user.refresh_token = keycloak_response['refresh_token']
            user.id_token = keycloak_response['id_token']
            user.save()
            return JsonResponse({'request': request.GET, 'response': keycloak_response})

    return JsonResponse(
        {'error': 'invalid_request', 'error_description': error_description}
    )
