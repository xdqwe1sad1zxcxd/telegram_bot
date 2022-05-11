from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

b1 = KeyboardButton('Об игре')
b2 = KeyboardButton('Создатели')
b3 = KeyboardButton('Для создателей')
b4 = KeyboardButton('Галерея')
b5 = KeyboardButton('help')
b6 = KeyboardButton('Герои')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client_admin.add(b1).insert(b2).row(b3, b4).insert(b6).row(b5)
kb_client.add(b1).insert(b2).row(b6, b4).insert(b5)
