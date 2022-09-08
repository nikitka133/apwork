from apwork.settings import CHAT_ROOT


def write_message(name_chat, message, author):
    """записывает сообщение в файл"""
    if name_chat:
        with open(CHAT_ROOT + name_chat + '.txt', 'a', encoding='utf-8') as file:
            print(name_chat)
            file.write(f'{author}: {message} \n')


def read_message(name_chat):
    """создает файл при первом обращение и читает все сообщения"""
    try:
        with open(CHAT_ROOT + name_chat + '.txt', encoding='utf-8') as file:
            message = file.readlines()
            return message
    except FileNotFoundError:
        open(CHAT_ROOT + name_chat + '.txt', 'w')


def check_filter_price(request):
    """проверяет запропрос что мин и макс диапазон цены фильтра не пустые"""
    if request['min_price'] and request['max_price']:
        return request['min_price'], request['max_price']
    elif request['min_price'] and not request['max_price']:
        return request['min_price'], '999999'
    elif not request['min_price'] and request['max_price']:
        return '0', request['max_price']
    else:
        return '0', '999999'
