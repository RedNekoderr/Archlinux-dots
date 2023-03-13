from aiogram import Dispatcher
from aiogram.types import Message
from datetime import datetime
from Handlers.tools import read_json_file
from Handlers.tools import write_to_json_file
from Handlers.tools import is_element_authorized
from Handlers.tools import send_error
from Handlers.tools import force_mute
from Handlers.tools import news


hour: int = 14


async def save_history(message: Message) -> None:
    '''Взаимодействия с сообщениями в чате'''
    global hour
    chat = message.chat
    user = message.from_user
    if (not await is_element_authorized(message.from_user.id,
                                        'Data/whitelist.json') and
            chat.type != 'private'):
        await message.delete()
        username = user.get_mention()
        bot_mention = '<b><a href="https://t.me/yegor_ice_bot">' + \
            'через бота</a></b>'
        err_not_autorized = (f'| {username}, чтобы общаться в чате, вы должны '
                             f'войти в него {bot_mention}')
        await force_mute(chat.id, user.id)
        await send_error(chat.id, err_not_autorized, sleep_duration=15)
        return
    history = await read_json_file('Data/history.json')
    if len(history) > 100:
        history.pop(1)
    history.append([user.id, message.message_id, message.text])
    await write_to_json_file(history, 'Data/history.json')
    current_hour = datetime.now().hour
    if current_hour == hour:
        if hour == 0:
            hour = 14
            return
        text = await news()
        hour = 0
        await send_error(message.chat.id, text, sleep_duration=5*60)


def register_general_handlers(dispatcher: Dispatcher) -> None:
    '''Регистрация комманд чата'''
    dispatcher.register_message_handler(save_history)
