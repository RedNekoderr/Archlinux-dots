from aiogram import Dispatcher
from aiogram import types
from aiogram.utils.exceptions import MessageToDeleteNotFound
from datetime import datetime
from datetime import timedelta
from Handlers.create_bot import bot
from Handlers.tools import change_json_file
from Handlers.tools import count_elements
from Handlers.tools import is_element_authorized
from Handlers.tools import force_unmute
from Handlers.tools import force_mute
from Handlers.tools import read_json_file
from Handlers.tools import read_json_list
from Handlers.tools import send_error
from Handlers.tools import write_to_json_file


async def ban_user(message: types.Message) -> None:
    '''
    Банит пользователя в чате по выделению его сообщения
    '''
    await message.delete()
    admin = message.from_user
    if not await is_element_authorized(admin.id,
                                       './Data/arch_admins.json'):
        return
    admin_mention = admin.get_mention(as_html=True)
    chat_id = message.chat.id
    if not message.reply_to_message:
        err_not_reply = (
            f'| {admin_mention}, '
            f'команда бана '
            f'должна быть ответом на '
            f'сообщение.'
        )
        await send_error(chat_id, err_not_reply)
        return
    ban_target = message.reply_to_message.from_user
    if await is_element_authorized(ban_target.id, './Data/arch_admins.json'):
        return
    reason = " ".join(message.text.split()[1:])
    if reason == '':
        err_wrong_parameters = (f'| '
                                f'{admin_mention}, не хватает '
                                f'параметров для бана.\n '
                                f'| Пример: "/ban причина".')
        await send_error(chat_id, err_wrong_parameters)
        return
    banned_person_data = await read_json_list('Data/banned.json',
                                              ban_target.id)
    username = ban_target.get_mention(as_html=True)
    if banned_person_data:
        err_alerady_banned = (f'| {admin_mention}, пользователь '
                              f'{username} уже забанен в чате')
        await send_error(chat_id, err_alerady_banned)
        return
    await message.answer(f'| <b>На пользователя '
                         f'{username} была наложена печать бана</b>\n'
                         f' | <b>Решение было принято:</b> {admin_mention}\n'
                         f' | <b>Причина:</b> {reason}',
                         parse_mode='html')
    await bot.ban_chat_member(chat_id,
                              ban_target.id)
    banned_person_data = [ban_target.id,
                          ban_target.first_name,
                          reason]
    try:
        await change_json_file(message.reply_to_message.from_user.id,
                               'Data/whitelist.json', remove=True)
    except ValueError:
        pass
    await change_json_file(banned_person_data, './Data/banned.json',
                           append=True)
    return


async def unban_user(message: types.Message) -> None:
    '''
    Снимает бан с пользователя по его ID, имени
    (первый встречный, начиная с конца списка забаненных)
    '''
    await message.delete()
    admin = message.from_user
    if not await is_element_authorized(admin.id,
                                       './Data/arch_admins.json'):
        return
    chat_id = message.chat.id
    admin_mention = admin.get_mention(as_html=True)
    banned_person = " ".join(message.text.split()[1:])
    if not banned_person:
        err_wrong_parameters = (f'| {admin_mention}, не '
                                f'хватает '
                                f'параметров для разбана.\n '
                                f'| Пример: "/unban имя/ID".')
        await send_error(chat_id, err_wrong_parameters)
        return
    if not (banned_person.isalpha() or banned_person.isdigit()):
        err_wrong_parameters_mesh = (f'| {admin_mention}, имя '
                                     f'или id '
                                     f'указаны неверно')
        await send_error(chat_id, err_wrong_parameters_mesh)
        return
    if banned_person.isdigit():
        banned_person = int(banned_person)
    banned_person_data: list | None = await \
        read_json_list('./Data/banned.json',
                       banned_person)
    if not banned_person_data:
        err_not_banned = (f'| {admin_mention}, '
                          f'пользователь '
                          f'{banned_person} не забанен '
                          f'в чате')
        await send_error(chat_id, err_not_banned)
        return
    username = (f'<a href="tg://user?id='
                f'{banned_person_data[0]}'
                f'">{banned_person_data[1]}</a>')
    await bot.unban_chat_member(chat_id, banned_person_data[0])
    await message.answer(f'| <b>С пользователя {username}'
                         f' была снята печать бана</b>\n | <b>'
                         f'Решение принято:</b> {admin_mention}',
                         parse_mode='html')
    await change_json_file(banned_person_data, 'Data/banned.json', remove=True)
    return


async def delete_many(message: types.Message) -> None:
    '''
    Удаляет все сообщения от пользовтеля от выделенного до последнего
    '''
    admin = message.from_user
    if not await is_element_authorized(admin.id,
                                       'Data/admins.json'):
        return
    chat_id = message.chat.id
    if not message.reply_to_message:
        await message.delete()
        await send_error(chat_id, 'Команда deleteall должна быть '
                         'ответом на сообщение')
        return
    message_id = message.reply_to_message.message_id
    user_id = message.reply_to_message.from_user.id
    messages = await read_json_file('Data/history.json')
    messages.reverse()
    for _ in range(10):
        for msg in messages:
            if msg[0] == user_id and msg[1] >= message_id:
                try:
                    await bot.delete_message(chat_id, msg[1])
                    messages.remove(msg)
                except MessageToDeleteNotFound:
                    messages.remove(msg)
    await write_to_json_file(messages, 'Data/history.json')
    await message.delete()
    return


async def delete_one(message: types.Message) -> None:
    '''Удаляет выделенное сообщение'''
    admin = message.from_user
    if not await is_element_authorized(admin.id,
                                       'Data/admins.json'):
        return
    chat_id = message.chat.id
    if not message.reply_to_message:
        await message.delete()
        await send_error(chat_id, 'Команда del должна быть '
                         'ответом на сообщение')
        return
    message_id = message.reply_to_message.message_id
    user_id = message.reply_to_message.from_user.id
    messages = await read_json_file('Data/history.json')
    messages.reverse()
    for _ in range(10):
        for msg in messages:
            if msg[0] == user_id and msg[1] == message_id:
                await bot.delete_message(chat_id, msg[1])
                messages.remove(msg)
                break
    await write_to_json_file(messages, './Data/history.json')
    await message.delete()
    return


async def warn_user(message: types.Message) -> None:
    '''
    Даёт предупреждение пользователю
    '''
    await message.delete()
    admin = message.from_user
    if not await is_element_authorized(admin.id,
                                       'Data/admins.json'):
        return
    admin_mention = admin.get_mention(as_html=True)
    chat_id = message.chat.id
    if not message.reply_to_message:
        err_not_reply = (f'| {admin_mention}, '
                         f'команда варна '
                         f'должна быть ответом на сообщение.')
        await send_error(chat_id, err_not_reply)
        return
    warn_target = message.reply_to_message.from_user
    if await is_element_authorized(warn_target.id,
                                   'Data/arch_admins.json'):
        return
    reason = " ".join(message.text.split()[1:])
    if not reason:
        err_wrong_parameters = (f'| '
                                f'{admin_mention}, не хватает '
                                f'параметров для варна.\n '
                                f'| Пример: "/warn причина".')
        await send_error(chat_id, err_wrong_parameters)
        return
    warn_target_message = message.reply_to_message
    warn_data = await read_json_list('Data/warns.json',
                                     warn_target_message.message_id)
    if warn_data:
        err_warn_exist = (f'| {admin_mention}, '
                          f'на данное сообщение '
                          f'уже существует жалоба')
        await send_error(chat_id, err_warn_exist)
        return
    warn_list = await read_json_file('Data/warns.json')
    warn_list.append([warn_target.id,
                      warn_target.first_name,
                      warn_target_message.message_id,
                      warn_target_message.text, reason])
    await write_to_json_file(warn_list, 'Data/warns.json')
    warns_amount = await count_elements('Data/warns.json',
                                        message.reply_to_message.from_user.id)
    username = warn_target.get_mention(as_html=True)
    await bot.send_message(chat_id, f'|<b>На сообщение пользователя '
                           f'{username}</b> была подана жалоба\n'
                           f' |<b>Решение было принято:</b> {admin_mention}\n'
                           f' |<b>Причина:</b> {reason}\n'
                           f' |<b>Колличество варнов: {warns_amount}</b>',
                           parse_mode='html',
                           reply_to_message_id=warn_target_message.message_id)
    return


async def mute_user(message: types.Message) -> None:
    '''Мутит пользователя на определённое время в чате'''
    await message.delete()
    admin = message.from_user
    if not await is_element_authorized(admin.id,
                                       'Data/admins.json'):
        return
    admin_mention = admin.get_mention(as_html=True)
    chat_id = message.chat.id
    if not message.reply_to_message:
        err_not_reply = (f'| {admin_mention}, '
                         f'команда мута '
                         f'должна быть ответом на '
                         f'сообщение.')
        await send_error(chat_id, err_not_reply)
        return
    mute_target = message.reply_to_message.from_user
    if await is_element_authorized(mute_target.id, 'Data/arch_admins.json'):
        return
    try:
        mute_duration = int(message.text.split()[1])
        mute_type = message.text.split()[2]
        mute_reason = " ".join(message.text.split()[3:])
        if mute_reason == '':
            err_no_reason = (f'| {admin_mention}, '
                             f'причина мута '
                             f'обязательна для указания')
            await send_error(chat_id, err_no_reason)
            return
    except (IndexError, ValueError):
        err_wrong_parameters = (f'| {admin_mention}, не '
                                f'хватает '
                                f'параметров для мута.\n '
                                f'| Пример: "/mute 1 h '
                                f'причина".')
        await send_error(chat_id, err_wrong_parameters)
        return
    mute_time_type = await define_words_end(mute_duration, mute_type)
    mute_time = await set_mute_time(mute_duration, mute_type)
    if not mute_time_type:
        err_wrong_time_format = (f'| {admin_mention}, вы ввели '
                                 f'неверный '
                                 f'формат времени.')
        await send_error(chat_id, err_wrong_time_format)
        return
    if not await mute_time_checker(mute_duration, mute_type, 1,
                                   message.from_user.id):
        mute_time_type = await define_words_end(mute_duration, 'd')
        err_not_enough_privileges = (f'| {admin_mention},'
                                     f'у вас нет возможности '
                                     f'выдавать мут более чем'
                                     f' на {mute_duration} '
                                     f'{mute_time_type}')
        await send_error(chat_id, err_not_enough_privileges)
        return
    username = mute_target.get_mention(as_html=True)
    await message.answer(f'|<b>На пользователя '
                         f'{username}</b> была наложена печать мута\n'
                         f' |<b>Решение было принято:</b> {admin_mention}\n'
                         f' |<b>Срок наказания:</b> {mute_duration} '
                         f'{mute_time_type}\n'
                         f' |<b>Причина:</b> {mute_reason}',
                         parse_mode='html')
    await force_mute(chat_id, mute_target.id,
                     mute_time)
    return


async def mute_time_checker(mute_duration: int, time_format: str,
                            time_limit: int, admin_id) -> bool:
    '''
    Проверяет, может ли админ мутить на время, больше данного
    '''
    is_time_arch: bool = False
    is_admin_arch: bool = await is_element_authorized(admin_id,
                                                      'Data/arch_admins.json')
    match time_format:
        case 'm':
            if mute_duration > 1440 * time_limit:
                is_time_arch = True
        case 'h':
            if mute_duration > 24 * time_limit:
                is_time_arch = True
        case 'd':
            if mute_duration > time_limit:
                is_time_arch = True
    if is_time_arch and not is_admin_arch:
        return False
    return True


async def set_mute_time(mute_duration: int, mute_type: str) -> float:
    '''Задаёт тип мута'''
    match mute_type:
        case 'm':
            timestamp = (datetime.now() +
                         timedelta(minutes=mute_duration)).timestamp()
        case 'h':
            timestamp = (datetime.now() +
                         timedelta(hours=mute_duration)).timestamp()
        case 'd':
            timestamp = (datetime.now() +
                         timedelta(days=mute_duration)).timestamp()
        case _:
            timestamp = 0.0
    return timestamp


async def define_words_end(mute_duration: int, mute_type: str) -> str:
    '''Определяет окончание формата времени'''
    last_number = int(str(mute_duration)[-1])
    match mute_type:
        case 'm':
            match last_number:
                case 1:
                    mute_time_type = 'минута'
                case 2 | 3 | 4:
                    mute_time_type = 'минуты'
                case _:
                    mute_time_type = 'минут'
        case 'h':
            match last_number:
                case 1:
                    mute_time_type = 'час'
                case 2 | 3 | 4:
                    mute_time_type = 'часа'
                case _:
                    mute_time_type = 'часов'
        case 'd':
            match last_number:
                case 1:
                    mute_time_type = 'день'
                case 2 | 3 | 4:
                    mute_time_type = 'дня'
                case _:
                    mute_time_type = 'дней'
        case _:
            mute_time_type = ''
    return mute_time_type


async def unmute_user(message: types.Message):
    await message.delete()
    admin = message.from_user
    if not await is_element_authorized(admin.id,
                                       'Data/admins.json'):
        return
    admin_mention = admin.get_mention(as_html=True)
    chat_id = message.chat.id
    if not message.reply_to_message:
        err_not_reply = (f'| {admin_mention}, '
                         f'команда размута '
                         f'должна быть ответом на '
                         f'сообщение.')
        await send_error(chat_id, err_not_reply)
        return
    unmute_target = message.reply_to_message.from_user
    if (await is_element_authorized(unmute_target.id,
                                    'Data/arch_admins.json') or
            await is_element_authorized(unmute_target.id, 'Data/admins.json')):
        return
    username = unmute_target.get_mention(as_html=True)
    await bot.send_message(chat_id,
                           f'| С пользователя {username} была снята '
                           f'печать мута\n | Решение принято: {admin_mention}',
                           parse_mode='html')
    await force_unmute(chat_id, unmute_target.id)
    return


def register_admin_handlers(dispatcher: Dispatcher) -> None:
    '''Регистрирует админские комманды в боте'''
    dispatcher.register_message_handler(ban_user, commands=['ban'])
    dispatcher.register_message_handler(mute_user, commands=['mute'])
    dispatcher.register_message_handler(unmute_user, commands=['unmute'])
    dispatcher.register_message_handler(unban_user, commands=['unbanid'])
    dispatcher.register_message_handler(delete_many,
                                        commands=['deleteall'])
    dispatcher.register_message_handler(delete_one, commands=['del'])
    dispatcher.register_message_handler(warn_user, commands=['warn'])
