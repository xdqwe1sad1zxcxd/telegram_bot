import json
import string
from random import choice

from aiogram import types, Dispatcher

answers = ['Я не знаю что на это ответить!',
           'Попробуй ввести какую-то команду!',
           'Повтори!',
           'Я не понимаю тебя!',
           'Такого ответа нет',
           'Затрудняюсь ответить на это!',
           ]


async def echo(message: types.message):               # проверка на мат
    """
    bad_words.json = файл в одной директории с main.py в котором в формате .json хранятся вся нецензурная лексика
    """
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}.intersection(
            set(json.load(open(f"bad_words.json")))) != set():
        await message.reply('В боте стоит фильтр на нецензурную лексику!')
        await message.delete()
    else:
        await message.reply(f"{choice(answers)}")


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo)
