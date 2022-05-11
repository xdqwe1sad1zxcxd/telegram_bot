from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

LOAD_BUTTON = KeyboardButton('new')
CANCEL_BUTTON = KeyboardButton('cancel')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(LOAD_BUTTON).insert(CANCEL_BUTTON)
