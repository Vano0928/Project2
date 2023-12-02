import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, CommandObject, state
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup

from loader import db_users, dp, keyboards


class RegStates(StatesGroup):

    first_name = State()
    last_name = State()


def get_user_data(telegram_user_id):
    user_data = db_users.get_user_by_telegram_id(telegram_user_id)

    
    first_name = user_data[2]
    last_name = user_data[3]
    username = user_data[1]
    english_level = user_data[-1]


    return f"""
Ваші дані:
Ім'я - {first_name}
Прізвище - {last_name}
Ім'я користувача - {username}
Рівень англійської - {english_level}
Якщо бажаєте змінити ваше ім'я або прізвище, то нажимайте:
Мій кабінет - Змінити мої дані
""".replace("None", "не визначено")


async def send_user_data(msg: types.Message):
    keyboard = keyboards.main_reply_kb()

    msg_to_user_text = get_user_data(msg.from_user.id)

    await msg.answer(msg_to_user_text, reply_markup=keyboard)


@dp.callback_query(F.data == "account_info")
async def callback_send_user_data(callback: types.CallbackQuery):

    msg_to_user_text = get_user_data(callback.from_user.id)
    keyboard = keyboards.back_to_my_cabinet()

    await callback.message.edit_text(msg_to_user_text, reply_markup=keyboard)


@dp.message(CommandStart())
async def add_user(msg: types.Message):
    await msg.reply("Привіт! Це бот по вивченню англійської. Тут ти зможеш пройти тестування по рівням англійської і підняти свій рівень англійської. А тепер уперед!",
                    reply_markup=keyboards.main_reply_kb())
    
    if not db_users.user_exists(msg.from_user.id):
        db_users.register_user(msg.from_user)
       
        await send_user_data(msg)

        keyboard = keyboards.main_test_kb()
        await msg.answer("Чи не бажаєте пройти тест по визначенню рівня англійсюкої мови?", reply_markup=keyboard)


@dp.callback_query(F.data == "get_user_info")
async def send_user_info(msg: types.Message):

    await send_user_data(msg)


@dp.callback_query(F.data == "edit_user_data")
async def edit_user_data(callback: types.CallbackQuery, state: FSMContext): 
    if await state.get_state():
        return
    
    user_data = db_users.get_user_by_telegram_id(callback.from_user.id)
    first_name = user_data[2]


    kb = [
       [types.KeyboardButton(text = f'{first_name}')]
       ]
    
    keyboard = keyboards.reply_kb_markup_generator(kb, "Введіть своє ім'я")
    
    await callback.message.reply("Напишіть своє ім'я", reply_markup=keyboard, parse_mode="MarkdownV2")
    await state.set_state(RegStates.first_name)


@dp.message(RegStates.first_name)
async def first_name_edit(msg: types.Message, state: FSMContext):
    first_name: str = msg.text

    if len(first_name.split()) == 1 and len(first_name) < 32:
        if first_name.isdigit():
            return


        user_data = db_users.get_user_by_telegram_id(msg.from_user.id)
        last_name = user_data[3]

        if last_name:

            kb = [
            [types.KeyboardButton(text = f'{last_name}')]
            ]
            
            keyboard = keyboards.reply_kb_markup_generator(kb, "Введіть своє прізвище")

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

        db_users.edit_user_data(msg.from_user.id, first_name, last_name, username)
        await send_user_data(msg)
        
        await state.clear()

    else:
        await msg.reply("Ви неправильно ввели своє прізвище")
