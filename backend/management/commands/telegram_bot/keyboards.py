from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from more_itertools import chunked

main_menu_buttons = {
    'program_button': '📋Программа',
    'cards_exchange_button': '🪪Обмен визитками',
    'asked_questions_button': '❓Мои вопросы',
    'ask_question_button': '🗣Задать вопрос спикеру',
    'donation_button': '💵Поддержать проект',
}

donation_buttons = {
    '100': '100 рублей',
    '150': '150 рублей',
    '300': '300 рублей',
    '500': '500 рублей',
    '1000': '1000 рублей',
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


def get_questions_keyboard(questions, chunk):
    chunk_size = 5
    chunked_requests = list(chunked(questions, chunk_size))

    arrows_keyboard = []
    arrows_keyboard.append(InlineKeyboardButton('⬅️', callback_data='⬅️')) \
        if chunk != 0 else None
    arrows_keyboard.append(InlineKeyboardButton('➡️', callback_data='➡️')) \
        if chunk + 1 != len(questions) else None
    keyboard = [
        arrows_keyboard,
        [InlineKeyboardButton('В главное меню', callback_data='back_to_menu')],
    ]

    return InlineKeyboardMarkup(keyboard)
