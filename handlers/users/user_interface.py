import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, CommandObject, state
from aiogram.fsm.state import State, StatesGroup

from loader import db_users, dp, keyboards


@dp.message(F.text == "Інформація")
async def info(msg: types.Message):

    await msg.reply("""
Що може цей бот?
 - Визначити твій рівень англійської
 - Допомогти прокачати свої знання
 - Давати рекомендації щодо вивчення нових слів та правил
 - Давати завдання
 - Допомогти тобі провести час із користю""")


@dp.message(F.text == "Мій кабінет")
async def my_cabinet(msg: types.Message):

    kb_markup = keyboards.my_cabinet_kb()
    await msg.reply("Ваш кабінет", reply_markup=kb_markup)


@dp.callback_query(F.data == "back_to_my_cabinet")
async def my_cabinet(callback: types.CallbackQuery):

    kb_markup = keyboards.my_cabinet_kb()
    await callback.message.edit_text("Ваш кабінет", reply_markup=kb_markup)


@dp.message(F.text == "Тести")
async def tests_choice(msg: types.Message):
    keyboard = keyboards.tests_choice_kb()
    await msg.reply("Виберіть тест", reply_markup=keyboard)


@dp.callback_query(F.data == "my_progress")
async def my_cabinet(callback: types.CallbackQuery):

    telegram_id = callback.from_user.id

    marks_data = db_users.get_marks(telegram_id)
    print(marks_data)
    if marks_data:
        marks_str = ''

        for mark in marks_data:
            marks_str += str(mark[0]) + ', '

        await callback.message.answer("Ваші оцінки:\n" + marks_str)
        db_users.add_mark(803678440, 10)
    
    else:

        await callback.message.answer("У вас ще немає оцінок")
        db_users.add_mark(803678440, 11)



