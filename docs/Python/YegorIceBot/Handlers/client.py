from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils.exceptions import CantRestrictChatOwner
from Handlers.Data import texts
from Handlers.keyboard import kb_client
from Handlers.keyboard import kb_empty
from Handlers.keyboard import kb_help
from Handlers.tools import change_json_file
from Handlers.tools import is_element_authorized
from Handlers.tools import force_unmute
from random import randint


class CaptchaForm(StatesGroup):
    '''Capthca form'''
    captcha = State()
    rules = State()


answer: int = 0


async def command_start(message: types.Message) -> None:
    '''/start command'''
    await message.delete()
    if message.chat.type == 'private':
        await message.answer('Добро пожаловать в чат\nЕгора Льда!',
                             reply_markup=kb_client)
    return


async def command_join(message: types.Message) -> None:
    '''Начало процедуры вхождения в чат'''
    if message.chat.type != 'private':
        return
    if await is_element_authorized(message.from_user.id,
                                   'Data/whitelist.json'):
        await message.answer('Вы уже в чате')
        return

    await message.answer('<b>| Капча</b>\n'
                         ' | Для попадания в чат вам нужно решить\n'
                         ' | простой пример, чтобы мы могли\n'
                         ' | удостовериться, что вы не робот\n',
                         reply_markup=kb_empty,
                         parse_mode='html')
    await captcha_send(message)
    await CaptchaForm.captcha.set()
    return


async def captcha_send(message: types.Message) -> None:
    global answer
    first_number, second_number = randint(0, 9), randint(0, 9)
    answer = first_number * second_number
    question = await define_number_as_word(first_number, second_number)
    await message.answer(f' | <b>Чему равно </b> '
                         f'"<i>{question}</i>"?\n'
                         f' | Ответ дать в виде числа (например 42)',
                         parse_mode='html', reply_markup=kb_empty)
    return


async def captcha_check(message: types.Message, state: FSMContext) -> None:
    '''Проверка капчи'''
    global answer
    if message.chat.type != 'private':
        return
    if message.text == 'Назад 🔙':
        await message.answer('Процедура вступления в чат прервана',
                             reply_markup=kb_client)
        await state.finish()
        return
    if not message.text.isdigit():
        await message.answer('Вы дали ответ в неверном '
                             'виде (Пример ответа: 42)',
                             reply_markup=kb_client)
        await state.finish()
        return
    if int(message.text) != answer:
        await message.answer(
            'Ответ неверный',
            reply_markup=kb_client)
        await state.finish()
        return
    await CaptchaForm.rules.set()
    await send_rules(message)
    await message.answer('Если вы согласны с правилами' +
                         ' напишите "Да"')
    return


async def accept_rules(message: types.Message,
                       state: FSMContext) -> None:
    '''Проверка согласия с правилами'''
    if message.text == 'Назад 🔙':
        await message.answer('Процедура вступления в чат прервана',
                             reply_markup=kb_client)
        return
    if message.text.lower() in 'да':
        await message.answer('Добро пожаловать... ' +
                             'Вы были добавлены в белый список ... ' +
                             '<ссылка на чат>', reply_markup=kb_client)
        await change_json_file(message.from_user.id, 'Data/whitelist.json',
                               append=True)
        try:
            await force_unmute(-1001415548796, message.from_user.id)
        except CantRestrictChatOwner:
            pass
    else:
        await message.answer('Ответ в случае отказа',
                             reply_markup=kb_client)
    await state.finish()


async def define_number_as_word(first_number: int, second_number: int) -> str:
    numbers = {
        0: 'ноль', 1: 'один', 2: 'два', 3: 'три', 4: 'четыре', 5: 'пять',
        6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять'
    }
    return numbers[first_number] + ' умножить на ' + \
        numbers[second_number]


async def command_links(message: types.Message) -> None:
    '''Show links'''
    if message.chat.type == 'private':
        await message.answer(
            texts.links, parse_mode='html',
            disable_web_page_preview=True)
    return


async def send_rules(message: types.Message) -> None:
    '''Show rules'''
    if message.chat.type == 'private':
        await message.answer(texts.rules, parse_mode='html')
    return


async def command_rules(message: types.Message) -> None:
    await send_rules(message)
    return


async def command_help(message: types.Message) -> None:
    await message.answer('Тут находится...', reply_markup=kb_help)


async def command_back(message: types.Message) -> None:
    await message.answer('Добро пожаловать в чат\nЕгора Льда!',
                         reply_markup=kb_client)


def register_client_handlers(dispatcher: Dispatcher) -> None:
    '''Registers client handlers'''
    dispatcher.register_message_handler(command_start, commands=['start'])
    dispatcher.register_message_handler(command_rules, text='Правила 📌')
    dispatcher.register_message_handler(command_join,
                                        text='Вступить в чат 🌀',
                                        state=None)
    dispatcher.register_message_handler(command_links, text='Ссылки 📋')
    dispatcher.register_message_handler(captcha_check,
                                        state=CaptchaForm.captcha)
    dispatcher.register_message_handler(accept_rules,
                                        state=CaptchaForm.rules)
    dispatcher.register_message_handler(command_help, text='Помощь 🆘')
    dispatcher.register_message_handler(command_back, text='Назад 🔙')
