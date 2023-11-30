import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, CommandObject, state
from aiogram.fsm.state import State, StatesGroup

from loader import db_users, dp


class RegStates(StatesGroup):

    first_name = State()
    last_name = State()


def reply_kb_markup_generator(kb: list, input_field_placeholder: str = None):

    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=input_field_placeholder
    )


async def send_user_data(msg: types.Message, telegram_id):
    user_data = db_users.get_user_by_telegram_id(msg.from_user.id)
    
    first_name = user_data[2]
    last_name = user_data[3]
    username = user_data[1]
    english_level = user_data[-1]



    msg_text = f"""
Ваші дані:
Ім'я - {first_name}
Прізвище - {last_name}
Ім'я користувача - {username}
Рівень англійської - {english_level}
Якщо бажаєте змінити ваше ім'я або прізвище, то нажимайте:
Мій кабінет - Змінити мої дані
"""

    await msg.answer(msg_text.replace("None", "не визначено"))



@dp.message(CommandStart())
async def add_user(msg: types.Message):
    await msg.reply("Привіт! Це бот по вивченню англійської. Тут ти зможеш пройти тестування по рівням англійської і підняти свій рівень англійської. А тепер уперед!")
    
    if not db_users.user_exists(msg.from_user.id):
        db_users.register_user(msg.from_user)

        user_id = msg.from_user.id        
        await send_user_data(msg, user_id)


@dp.message(F.text == "Змінити мої дані")
async def edit_user_data(msg: types.Message, state: FSMContext):
    if await state.get_state():
        return
    
    user_data = db_users.get_user_by_telegram_id(msg.from_user.id)
    first_name = user_data[2]


    kb = [
       [types.KeyboardButton(text = f'{first_name}')]
       ]
    
    keyboard = reply_kb_markup_generator(kb, "Введіть своє ім'я")

    await msg.reply("Напишіть своє ім'я", reply_markup=keyboard)
    await state.set_state(RegStates.first_name)


@dp.message(RegStates.first_name)
async def first_name_edit(msg: types.Message, state: FSMContext):
    first_name = msg.text

    if len(first_name.split()) == 1 and len(first_name) < 32:

        user_data = db_users.get_user_by_telegram_id(msg.from_user.id)
        last_name = user_data[3]
        print(last_name)
        if last_name:

            kb = [
            [types.KeyboardButton(text = f'{last_name}')]
            ]
            
            keyboard = reply_kb_markup_generator(kb, "Введіть своє прізвище")

        else:
            keyboard= types.ReplyKeyboardRemove()

        await msg.reply('Тепер введіть ваше прізвище', reply_markup=keyboard, parse_mode="MarkdownV2")    

        await state.update_data({"first_name" : first_name})
        await state.set_state(RegStates.last_name)

    else:
        await msg.reply("Ви неправильно ввели своє імя")


@dp.message(RegStates.last_name)
async def user_edit(msg: types.Message, state: FSMContext):
    if len(msg.text.split()) == 1 and len(msg.text) < 32:

        user_data = await state.get_data()
        first_name = user_data["first_name"]
        last_name = msg.text
        username = msg.from_user.username
        user_id = msg.from_user.id

        db_users.edit_user_data(msg.from_user.id, first_name, last_name, username)
        await send_user_data(msg, user_id)
        
        await state.clear()

    else:
        await msg.reply("Ви неправильно ввели своє прізвище")
