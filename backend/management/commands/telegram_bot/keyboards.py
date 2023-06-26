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


def get_lists_of_buttons(buttons, rows_quantity):
    for button_number in range(0, len(buttons), rows_quantity):
        yield buttons[button_number: button_number + rows_quantity]


def get_keyboard(buttons, rows_quantity):
    reply_markup = ReplyKeyboardMarkup(
        keyboard=list(get_lists_of_buttons(buttons, rows_quantity)),
        resize_keyboard=True
    )
    return reply_markup


def get_arrows_keyboard(chunks, chunk):
    arrows_keyboard = []
    if chunks:
        arrows_keyboard.append(InlineKeyboardButton('⬅️', callback_data='⬅️')) \
            if chunk != 0 else None
        arrows_keyboard.append(InlineKeyboardButton('➡️', callback_data='➡️')) \
            if chunk + 1 != len(chunks) else None
    keyboard = [
        arrows_keyboard,
        [InlineKeyboardButton('В главное меню', callback_data='back_to_menu')],
    ]

    return InlineKeyboardMarkup(keyboard)
