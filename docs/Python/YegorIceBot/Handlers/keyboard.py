from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
# from aiogram.types import ReplyKeyboardRemove

button_links = KeyboardButton('Ссылки 📋')
button_start = KeyboardButton('Вступить в чат 🌀')
button_rules = KeyboardButton('Правила 📌')
button_help = KeyboardButton('Помощь 🆘')
button_q = KeyboardButton('Вопросы к администрации ❓')
button_back = KeyboardButton('Назад 🔙')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(button_start).add(button_help).insert(
    button_rules)

kb_help = ReplyKeyboardMarkup(resize_keyboard=True)
kb_help.add(button_q).add(button_links).insert(button_back)

kb_empty = ReplyKeyboardMarkup(resize_keyboard=True)
kb_empty.add(button_back)
