from django.utils.module_loading import import_module

workflow_states = (
    'reset',
    'start',
    'echo',
)


def load_func(state):
    module = import_module(f'telegram_bot.workflow.states.{state}')
    return module


states = {state: load_func(state) for state in workflow_states}
print(states['start'].prepare)
