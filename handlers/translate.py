# import logging

# from aiogram import types, Router, F
# from aiogram.fsm.context import FSMContext
# from aiogram.filters import Command, CommandStart, CommandObject, state
# from aiogram.filters.callback_data import CallbackData
# from aiogram.fsm.state import State, StatesGroup

# from googletrans import Translator

# from loader import dp, keyboards

# class Translate_State(StatesGroup):
#     translate = State()


# def translate(text, scr: str, dest: str):
#     translator = Translator()

#     translated = translator.translate(text, scr, dest)

#     return translated


# @dp.message(F.text == "Перекласти")
# async def translate_to_user(msg: types.Message):
#     keyboard = keyboards.get_translate_kb()

#     await msg.reply("Виберіть, якою мовою ви хочете перекласти", reply_markup=keyboard)



# @dp.callback_query(F.data.in_(["ua_to_us", "us_to_ua"]))
# async def translate_check(callback: types.CallbackQuery, state: FSMContext):
#     await callback.message.answer("Напишіть текст, щоб перекласти")

#     await state.set_state(Translate_State.translate)
#     await state.update_data({"translation" : f"{callback.data}"})


# @dp.message(Translate_State.translate)
# async def msg_translate(msg: types.Message, state: FSMContext):
#     user_text = msg.text
#     state_data = await state.get_data()
#     translation = state_data["translation"]

#     if translation == "en_to_ua":
#         translated_text = translate(user_text, "uk", "en")

#     else:
#         translated_text = translate(user_text, "en", "uk")

#     await msg.answer(translated_text.text)
