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
