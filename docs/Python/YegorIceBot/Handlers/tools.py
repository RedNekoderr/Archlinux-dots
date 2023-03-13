'''
Инструменты для работы бота
'''
from aiogram.types import ChatPermissions
from asyncio import sleep
from datetime import datetime
from datetime import timedelta
from random import randint
from json import dump as jsdump
from json import load as jsload

from Handlers.create_bot import bot


async def read_json_file(file_name: str) -> list:
    '''
    Возращает список в json файле как list[Any]
    '''
    with open(file_name, encoding='utf-8') as read:
        return jsload(read)


async def read_json_list(file_name: str, element) -> list | None:
    '''
    Читает list[list] и возращает первый подходящий элемент, если такой
    найдётся в внутреннем списке или None, если такго не будет
    '''
    targer_data = await read_json_file(file_name)
    targer_data.reverse()
    for data_list in targer_data:
        if element in data_list:
            return data_list
    return


async def count_elements(file_name: str, element) -> int:
    '''
    Считает колличество элементов в списке
    '''
    counter: int = 0
    for data_list in await read_json_file(file_name):
        if element in data_list:
            counter += 1
    return counter


async def write_to_json_file(element: list, file_name: str) -> None:
    '''
    Записывает list в json файл
    '''
    with open(file_name, 'w', encoding='utf-8') as write:
        jsdump(element, write)
    return


async def change_json_file(element, file_name: str,
                           remove: bool = False, append: bool = False) -> None:
    '''
    Добавляет list в json файл
    '''
    local_list: list = await read_json_file(file_name)
    if append:
        local_list.append(element)
    if remove:
        local_list.remove(element)
    await write_to_json_file(local_list, file_name)
    return


async def is_element_authorized(element: int, file_name: str) -> bool:
    '''
    Проверяет наличие элемента в json файле
    '''
    if element in await read_json_file(file_name):
        return True
    return False


async def send_error(chat_id: int, message: str,
                     sleep_duration: int = 5) -> None:
    '''
    Отправляет сообщение об ошибке для админа и удаляет его через
    определённое количестов секунд
    '''
    error_message = await bot.send_message(chat_id, message, parse_mode='html')
    await sleep(sleep_duration)
    await error_message.delete()
    return


async def force_mute(chat_id, user_id, limit=None) -> None:
    if limit:
        await bot.restrict_chat_member(chat_id, user_id,
                                       ChatPermissions(False),
                                       until_date=limit)
        return
    await bot.restrict_chat_member(chat_id, user_id,
                                   ChatPermissions(False))
    return


async def force_unmute(chat_id, user_id) -> None:
    timestamp = (datetime.now() +
                 timedelta(minutes=1)).timestamp()
    await bot.restrict_chat_member(
        chat_id, user_id,
        ChatPermissions(can_send_messages=True,
                        can_send_photos=True,
                        can_send_videos=True,
                        can_send_video_notes=True,
                        can_send_audios=True,
                        can_send_voice_notes=True,
                        can_send_documents=True,
                        can_send_other_messages=True,
                        can_send_polls=True))
    await force_mute(chat_id, user_id, limit=timestamp)
    return


async def news():
    texts = {
        1: 'Нравится общаться?\nНам тоже!\nЗа это можно поблагодарить \
            администрацию и дать им немножечко на покушать:  ' +
        '<a href="https://www.donationalerts.com/r/yegor_lda">-=Донат=-</a>',
        2: 'Нравится общаться?\nА мы следим за порядком в чате 24/7...\n' +
        'За это можно поблагодарить \
                администрацию и дать им немножечко на покушать:  ' +
        '<a href="https://www.donationalerts.com/r/yegor_lda">-=Донат=-</a>'
    }
    message = texts[randint(1, 2)]
    return message
