from django.utils.module_loading import import_module

workflow_states = (
    'disabled',
    'ready',
    'test_echo',
)


def load_func(state):
    module = import_module(f'telegram_bot.workflow.states.{state}')
    return module


states = {state: load_func(state) for state in workflow_states}
