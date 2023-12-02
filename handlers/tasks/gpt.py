import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, CommandObject, state
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup

from openai import OpenAI
import re

from loader import db_users, dp, keyboards, OPENAI_API_KEY

from . prompt import get_prompt


class text_translate_states(StatesGroup):
    translating = State()


def chatgpt_response(prompt):
    client = OpenAI(

        api_key=OPENAI_API_KEY
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content


@dp.message(F.text == "Завдання")
async def task(msg: types.Message, state: FSMContext):

    with open("C:\\Users\\user\\Desktop\\python_projects\\Project2\\handlers\\tasks\\prompts\\message.txt", mode="r", encoding="utf-8") as file:
        message_to_user = file.read()

    await msg.reply(message_to_user)

    keyboard = keyboards.choose_sentence_number_kb()
    await msg.answer("Виберіть скільки речень буде у тексті", reply_markup=keyboard)
    db_users.add_mark(msg.from_user.id, 11)


@dp.callback_query(F.data.in_(("2", "4", "6")))
async def send_english_text(callback: types.CallbackQuery, state: FSMContext):
    prompt = f"Напиши твір англійською мовою на довільну тему, {callback.data} речень"

    await callback.message.answer("Зачекайте декілька секунд, будь ласка")
    english_text = chatgpt_response(prompt)

    await callback.message.answer(f"Перекладіть текст:\n{english_text}")
    await state.set_state(text_translate_states.translating)
    await state.update_data({"english_text" : english_text})
    


@dp.message(text_translate_states.translating)
async def check_translated_text(msg: types.Message, state: FSMContext):
    data: dict = await state.get_data()
    english_text = data["english_text"]

    translated_text = msg.text

    prompt = get_prompt(english_text, translated_text)

    await msg.answer("Зачекайте декілька секунд, будь ласка")
    chatgpt_answer = chatgpt_response(prompt)

    await msg.answer(chatgpt_answer)


    match = re.search(r'\d+', chatgpt_answer)
    if match:
        middle_number = int(match.group())

    telegram_id = msg.from_user.id

    db_users.add_mark(telegram_id, middle_number)
