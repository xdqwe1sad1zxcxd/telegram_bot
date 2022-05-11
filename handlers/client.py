import os
import json
from random import choice

from aiogram import types, Dispatcher

from bot_config import bot
from handlers import send_hi, admin
from keyboard import kb_client, kb_admin, kb_client_admin


async def send_start(message: types.message):
    await bot.send_message(message.from_user.id, f"{send_hi.start_text}", reply_markup=kb_client if message.from_user.id not in admin.IDs else kb_client_admin)


async def bot_commands(message: types.message):
    await bot.send_message(message.from_user.id, f"{send_hi.commands}", reply_markup=kb_client if message.from_user.id not in admin.IDs else kb_client_admin)


async def get_back(message: types.message):
    await bot.send_message(message.from_user.id, f"Отменил текущее действие!", reply_markup=kb_client if message.from_user.id not in admin.IDs else kb_client_admin)


async def about_authors(message: types.message):
    directory = r"D:\Tg_bot\authors"

    author1 = 'Данёк.json'

    with open(f"{directory}\\{author1}", 'rb') as file:
        author_descr1 = json.load(file)
        await bot.send_photo(message.from_user.id, photo=author_descr1['PHOTO'],
                             caption=f"Имя создателя бота: {author1.split('.')[0]}\n=====\nО себе: {author_descr1['DESCRIPTION']}")


async def about_game(message: types.message):
    await bot.send_message(message.from_user.id,
                           f"Будущая pixel indi game в жанре MMORPG, сделанная на простом движке, простой девочкой!")


async def send_heroes(message: types.message):
    try:
        directory = r"D:\Tg_bot\description_heroes"
        hero = choice([hero for hero in os.listdir(directory)])
        with open(f"{directory}\\{hero}", 'rb') as file:
            hero_descr = json.load(file)
            await bot.send_photo(message.from_user.id, photo=hero_descr['PHOTO'], caption=f"Имя персонажа: {hero.split('.')[0]}\n=====\nОписание: {hero_descr['DESCRIPTION']}")
    except Exception as ex:
        await bot.send_message(5167573237, f"WARNING: ошибка в боте {ex}")
        await bot.send_message(message.from_user.id, f"Упс... похоже описание героев пустое и мне нечего вам отправить!")


async def choserandomimg(message: types.message):
    try:
        directory = r"D:\Tg_bot\галерея"
        image = choice([img for img in os.listdir(directory)])
        await bot.send_photo(message.from_user.id, photo=open(f"{directory}\\{image}", 'rb'))
    except Exception as ex:
        await bot.send_message(5167573237, f"WARNING: ошибка в боте {ex}")
        await bot.send_message(message.from_user.id, f"Упс... похоже галерея пуста или произошла ошибка.")


async def for_creators(message: types.message):
    if message.from_user.id in admin.IDs:
        await bot.send_message(message.from_user.id, f"{send_hi.for_admins}", reply_markup=kb_admin)
    else:
        await message.reply(
            f"Прошу прощения, но вы не состоите в списке создателей. У меня нет полномочий показывать вам этот раздел!")
        await message.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_start,
                                lambda message: message.text.lower().strip() in ['start', '/start'])
    dp.register_message_handler(bot_commands,
                                lambda message: message.text.lower().strip() in ['help', 'commands', '/help', '/commands'])
    dp.register_message_handler(get_back,
                                lambda message: message.text.lower().strip() in ['назад', 'cancel', '/cancel', ])
    dp.register_message_handler(about_authors,
                                lambda message: message.text.lower().strip() in ['создатели', '/создатели', 'about_authors', '/about_authors'])
    dp.register_message_handler(about_game,
                                lambda message: message.text.lower().strip() in ['об игре', '/об игре', 'about_game', '/about_game'])
    dp.register_message_handler(send_heroes,
                                lambda message: message.text.lower().strip() in ['heroes', '/heroes', 'герои', '/герои'])
    dp.register_message_handler(choserandomimg,
                                lambda message: message.text.lower().strip() in ['галерея', '/галерея', '/gallery', 'gallery'])
    dp.register_message_handler(for_creators,
                                lambda message: message.text.lower().strip() in ['для создателей', '/для создателей', 'commands_', '/commands_'])
