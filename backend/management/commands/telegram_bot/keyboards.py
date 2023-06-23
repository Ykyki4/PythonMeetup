from telegram import KeyboardButton, ReplyKeyboardMarkup

main_menu_buttons = {
    'program_button': '📋Программа',
    'cards_exchange_button': '🪪Обмен визитками',
    'my_question_button': '❓Мои вопросы',
    'donation_button': '💵Поддержать проект',
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
