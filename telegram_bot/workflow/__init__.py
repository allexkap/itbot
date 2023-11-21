import yaml
from django.utils.module_loading import import_module

from itbot.settings import BASE_DIR


def parse_schema(schema, path):
    result = []
    for entry in schema:
        if isinstance(entry, str):
            result.append(f'{path}.{entry}')
        else:
            ((sub, entry),) = entry.items()
            result.extend(parse_schema(entry, f'{path}.{sub}'))
    return result


with open(BASE_DIR / 'telegram_bot' / 'workflow' / 'config.yaml') as file:
    schema = yaml.load(file.read(), Loader=yaml.Loader)

paths = parse_schema(schema['states'], 'telegram_bot.workflow.states')

states = {state[29:].replace('.', '/'): import_module(state) for state in paths}
