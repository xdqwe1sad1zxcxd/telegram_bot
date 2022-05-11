import json

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_config import bot
from cfg import admins_ids
from keyboard import kb_admin, kb_client

IDs = admins_ids

hero_discr = {'PHOTO': '',
              'NAME': '',
              'DESCRIPTION': ''}


class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    description = State()


async def cm_start(message: types.message):
    if message.from_user.id in IDs:
        await FSMadmin.photo.set()
        await message.reply('Загрузи фото', reply_markup=kb_admin)
    else:
        await message.reply(f"Команда доступна только для модераторов!")
        await message.delete()


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in IDs:
        current_state = await state.get_state()
        if current_state is None:
            return
        await message.reply('Хорошо, я отменил ваш выбор!', reply_markup=kb_client)
        await state.finish()


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id in IDs:
        if message.content_type != 'photo':
            await bot.send_message(message.from_user.id, 'Это не фото! Отправьте фото!')
            return
        else:
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
                hero_discr['PHOTO'] = data['photo']
        await FSMadmin.next()
        await message.reply("Теперь название!")


async def load_name(message: types.message, state: FSMContext):
    if message.from_user.id in IDs:
        async with state.proxy() as data:
            data['name'] = message.text
            hero_discr['NAME'] = data['name']
        await FSMadmin.next()
        await message.reply("Хорошо, какое сделаем описание?")


async def load_description(message: types.message, state: FSMContext):
    if message.from_user.id in IDs:
        try:
            async with state.proxy() as data:
                data['description'] = message.text
                hero_discr['DESCRIPTION'] = data['description']
            async with state.proxy() as data:
                await message.reply(f"Имя: {data['name']}\nОписание: {data['description']}")
            await bot.send_message(message.from_user.id,
                                   f"Описание готово и добавлено в базу данных!", reply_markup=kb_client)
            await state.finish()
            with open(f"description_heroes/{hero_discr['NAME']}.json", 'w', encoding='UTF-8') as file:
                json.dump(hero_discr, file, indent=4)
        except AttributeError:
            await bot.send_message(message.from_user.id, f"Что-то пошло не так, описание не добавлено...",
                                   reply_markup=kb_client)
            await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, lambda message: message.text.lower().strip() in ['new', '/new'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMadmin.photo)
    dp.register_message_handler(load_photo, state=FSMadmin.photo)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_description, state=FSMadmin.description)
