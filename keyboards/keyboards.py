from aiogram import types
from aiogram.filters.callback_data import CallbackData

class KButton(types.KeyboardButton):
    pass

class IKButton(types.InlineKeyboardButton):
    pass


class Keyboards:

    def __init__(self) -> None:
        pass

    def reply_kb_markup_generator(self, keyboard: list, input_field_placeholder: str = None):

        return types.ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            input_field_placeholder=input_field_placeholder
    )


    def inline_kb_markup_generator(self, keyboard: list):

        return types.InlineKeyboardMarkup(inline_keyboard=keyboard)


    def main_reply_kb(self):
        keyboard= [[KButton(text="Мій кабінет"), KButton(text="Інформація")],
                   [KButton(text="Тести"), KButton(text="Завдання")],
                   [KButton(text="Перекласти"), KButton(text="Вивчити")]
                   ]
        
        return self.reply_kb_markup_generator(keyboard)
    

    def my_cabinet_kb(self):
        keyboard = [
            [IKButton(text="Інформація про акаунт", callback_data="account_info")],
            [IKButton(text="Змінити дані", callback_data="edit_user_data"),
             IKButton(text="Мій прогрес", callback_data="my_progress")]
            ]
        
        return self.inline_kb_markup_generator(keyboard)
    

    def back_to_my_cabinet(self):
        keyboard = [
            [IKButton(text="Назад", callback_data="back_to_my_cabinet")]
            ]
        
        return self.inline_kb_markup_generator(keyboard)
    

    def main_test_kb(self):

        keyboard = [
            [IKButton(text="Так", callback_data="start_main_test")]
            ]
        
        return self.inline_kb_markup_generator(keyboard)
    

    def tests_choice_kb(self):

        keyboard= [
            [IKButton(text="Визначення рівня англійської", callback_data="start_main_test")],
            [IKButton(text="Тест1", callback_data="test1"), IKButton(text="Тест2", callback_data="test2")]
            ]
        
        return self.inline_kb_markup_generator(keyboard)
    

    def choose_sentence_number_kb(self):
        keyboard = [
            [IKButton(text="2", callback_data="2"), IKButton(text="4", callback_data="4"), IKButton(text="6", callback_data="6")]
        ]
        
        return self.inline_kb_markup_generator(keyboard)
    

    def get_translate_kb(self):

        keyboard = [
            [IKButton(text="На англійську", callback_data="ua_to_us"), IKButton(text=":На українську", callback_data="us_to_ua")]
        ]

        return self. inline_kb_markup_generator(keyboard)