## Workflow States
### Введение
Основная идея этой реализации - максимальная гибкость и удобство написания новых состояний.  
Любая вспомогательная логика и частые конструкции могут быть помещены в файл `utils.py`.

### Описание
В каждом состоянии нужно реализовать две функции:
```py
def prepare(update: Update, context: CallbackContext, user: User) -> None | str:
    pass

def process(update: Update, context: CallbackContext, user: User) -> None | str:
    pass
```

- `prepare` - вызывается при переходе в состояние  
  Чаще всего используется для вывода приветственного сообщения,
  которое описывает, что бот ждет от пользователя  
  Возвращает не `None`, если переход не одобрен
- `process` - вызывается для обработки действия этим состоянием  
  Отвечает за переход в другое состояние  
  Возвращает требуемое следующее состояние в строком формате или `None`,
  если переход не требуется


### Примеры
Для удобства разработки созданы функции `get_markup`
и декоратор `parse_commands`.  
Оба на вход они принимают список объектов Edge.

В примере ниже, бот при переходе в данное состояние отправит сообщение и
установит клавиатуру с одной кнопкой с текстом, который будет взят из базы
данных по `string_id_from_db`. После он будет ждать либо сообщение с
этим текстом, либо команду `/start`.  
После их получения перейдет в состояние `ready`.
```py
from telegram_bot.workflow.utils import *

edges = [
    Edge(next_state='ready', cmd='start', text='string_id_from_db'),
]

def prepare(update: Update, context: CallbackContext, user: User) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='string_id_from_db',
        reply_markup=get_markup(edges),
    )

@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> None | str:
    pass
```
Функция с декоратором `parse_commands` выполняется как обычно,
если подходящий переход не найден.

`next_state` может быть не только строкой, но и вызываемым объектом.
Тогда следующим состоянием становится результат его вызова.
Используется, если команду надо обработать, а в отдельное состояние
переходить смысла нет.
```py
def _help(update: Update, context: CallbackContext, user: User) -> None | str:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='string_id_from_db',
    )

edges = [
    Edge('ready', 'cancel'),
    Edge(_help, 'help'),
]
```

Так как отправлять сообщение и менять клавиатуру это самый частый паттерн
использования `prepare`, то была реализована функция `send_message_with_reply_keyboard`.  
Тогда пример выше может быть переписан в:
```py
from telegram_bot.workflow.utils import *

edges = [
    Edge(next_state='ready', cmd='start', text='string_id_from_db'),
]

prepare = send_message_with_reply_keyboard('string_id_from_db', edges)

@parse_commands(edges)
def process(update: Update, context: CallbackContext, user: User) -> None | str:
    pass
```

### Контекст пользователя
Для передачи данных между состояниями реализованы следующие методы класса `User`:
```py
user.set_property(name: str, value: str) -> None:
user.get_property(name: str) -> str | None:
user.clear_properties() -> None:
```
