from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from loader import dp, bot, db_users, keyboards
import json


tests_path = "C:\\Users\\user\\Desktop\\python_projects\\Project2\\handlers\\tests\\questions\\"


with open(f'{tests_path}start_test.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

    main_test_ques = json_data


with open(f'{tests_path}test1.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

    test1_ques = json_data


with open(f'{tests_path}test2.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

    test2_ques = json_data


class TestStates(StatesGroup):
    start_of_test = State()
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    q9 = State()
    q10 = State()
    final_q = State()


test_states_order = {i: getattr(TestStates, f'q{i}') for i in range(1, 11)}


def dynamic_reply_db(answers: list):

    if answers == 3:
        keyboard = types.ReplyKeyboardMarkup(
            keyboard = [
                [types.KeyboardButton(text=answer) for answer in answers[:2]],
                [types.KeyboardButton(text=answers[2]) ] 
            ], resize_keyboard=True
        )

    else:

        keyboard = types.ReplyKeyboardMarkup(
            keyboard = [
                [types.KeyboardButton(text=answer) for answer in answers[:2]],
                [types.KeyboardButton(text=answer) for answer in answers[2:]] 
            ], resize_keyboard=True
        )

    return keyboard



def question_generator(prev_number, curr_number, state_name, next_state, ques):
    @dp.message(state_name, F.text.in_(ques[prev_number]['options']))
    async def question(msg: types.Message, state: FSMContext):

        our_data = await state.get_data()
        if msg.text == ques[prev_number]["right_answer"]:
            await state.update_data(
                {
                    "score":our_data['score'] + 1,
                    f"answer_{prev_number}": f"Y Ви відповіли правильно! Відповідь: {ques[prev_number]['right_answer']}"
                }

            )
        else:
            await state.update_data(
                {
                    f"answer_{prev_number}": f"X Ви відповіли НЕправильно! Правильна відповідь: {ques[prev_number]['right_answer']}"
                }

            )

        await msg.answer(f"Відповідь зарахована")
        await msg.answer(f"{curr_number} Питання:")
        await msg.answer(ques[curr_number]["question"], reply_markup=dynamic_reply_db(ques[curr_number]["options"]))
        await state.set_state(next_state)


def generate_init_questions(ques_number, ques):
    curr_number = 2 # тому, що у test_states_order перший state - q2, а першого немає

    while True:
        prev_number = curr_number - 1
        next_number = curr_number + 1

        if next_number == ques_number:
            question_generator(f"{prev_number}", f"{curr_number}", test_states_order[curr_number], TestStates.final_q, ques)
            break

        question_generator(f"{prev_number}", f"{curr_number}", test_states_order[curr_number], test_states_order[next_number], ques)
        curr_number += 1


generate_init_questions(11, main_test_ques)
generate_init_questions(10, test1_ques)
generate_init_questions(8, test2_ques)


async def start_test(callback: types.CallbackQuery, state: FSMContext, ques):
    if db_users.user_exists(callback.from_user.id) is not None:
        await callback.message.answer("Привіт, починаємо тест!")
        await state.update_data(score=0)
        await callback.message.answer(f"1 Питання:")
        await callback.message.answer(ques["1"]["question"], reply_markup=dynamic_reply_db(ques["1"]["options"]))
        await state.set_state(TestStates.q2)

    else:
        await callback.message.answer("Зареєструйся!")


@dp.callback_query(F.data == "start_main_test")
async def first_main_question(callback: types.CallbackQuery, state: FSMContext):
    await start_test(callback, state, main_test_ques)


@dp.callback_query(F.data == "test1")
async def test1_start_question(callback: types.CallbackQuery, state: FSMContext):
    await start_test(callback, state, test1_ques)


@dp.callback_query(F.data == "test2")
async def test1_start_question(callback: types.CallbackQuery, state: FSMContext):
    await start_test(callback, state, test2_ques)


async def test_result(msg: types.Message, state: FSMContext):

    user_test_data: dict = await state.get_data()

    del user_test_data["score"]

    message_to_user = "Ваші результати:\n"

    for answer_text in user_test_data.values():

        message_to_user += answer_text + "\n"

    await msg.answer(message_to_user)


@dp.message(TestStates.final_q)
async def my_test(msg: types.Message, state: FSMContext):
    our_data = await state.get_data()

    score = our_data['score']
    english_level = "A1"
    if score == 0:
        await msg.answer("У тебе A0, біжи вчитись!")
        english_level = "A0"
    elif score > 3:
        english_level = "A2"
    elif score > 6:
        english_level = "B1"
    elif score > 9:
        english_level = "B2"

    telegram_id = msg.from_user.id
    db_users.update_english_level(telegram_id, english_level)

    keyboard = keyboards.main_reply_kb()
    await msg.answer(f"Тест закінчено! Твій рівень {english_level}\nТвій результат - {score}/{len(main_test_ques)}", reply_markup=keyboard)



    await test_result(msg, state)
    await state.clear()