from telegram import KeyboardButton, ReplyKeyboardMarkup

main_menu_buttons = {
    'program_button': '📋Программа',
    'ask_question_button': '🗣Задать вопрос спикеру',
    'my_question_button': '❓Мои вопросы',
}

def set_keyboards_buttons(buttons):
    keyboard = []

    for button in buttons:
        keyboard.append(KeyboardButton(button))

    return keyboard


def get_keyboard(buttons, one_time_keyboard=False):
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[set_keyboards_buttons(buttons)],
        resize_keyboard=True,
        one_time_keyboard=one_time_keyboard,
    )
    return reply_markup