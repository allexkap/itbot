## Workflow States
### Описание
В каждом состоянии нужно реализовать две функции:
```py
def prepare(update: Update, context: CallbackContext) -> None | str:
    pass

def process(update: Update, context: CallbackContext) -> None | str:
    pass
```

- `prepare` - вызывается при переходе в состояние  
  Чаще всего используется для вывода приветственного сообщения, которое описывает, что бот ждет от пользователя
- `process` - вызывается для обработки действия этим состоянием  
  Отвечает за переход в другое состояние

### Возвращаемые значения
#### Prepare
**В ПРОЦЕССЕ РАЗРАБОТКИ**  
Возвращает не `None`, если переход не одобрен
#### Process
Возвращает требуемое следующее состояние в строком формате или `None`, если переход не требуется

### Диалоговый режим
Для удобства разработки созданы функция `get_markup` и декоратор `parse_commands`.
Оба на вход они принимают список объектов Edge.

В примере ниже, бот при переходе в данное состояние отправит сообщение и установит клавиатуру
с кнопкой 'Привет'. После он будет ждать либо сообщение с этим текстом, либо команду `/start`.
После их получения перейдет в состояние `ready`.
```py
from .utils import *

edges = [
    Edge(next_state='ready', cmd='start', text='Привет'),
]

def prepare(update: Update, context: CallbackContext) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Placeholder",
        reply_markup=get_markup(edges),
    )

@parse_commands(edges)
def process(update: Update, context: CallbackContext) -> None | str:
    pass
```
Функция с декоратором `parse_commands` выполняется как обычно, если подходящий переход не найден.

`next_state` может быть не только строкой, но и вызываемым объектом.
Тогда следующим состоянием становится результат его вызова.
Используется, если команду надо обработать, а в отдельное состояние переходить смысла нет.
```py
def _help(update: Update, context: CallbackContext) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="`//cancel` to suppress command",
        parse_mode=ParseMode.MARKDOWN_V2,
    )

edges = [
    Edge('ready', 'cancel'),
    Edge(_help, 'help'),
]
```
