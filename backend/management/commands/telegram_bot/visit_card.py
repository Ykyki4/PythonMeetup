import textwrap
from enum import Enum

from more_itertools import chunked
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .keyboards import get_arrows_keyboard
from .main_menu import send_main_menu
from backend.utils import get_visit_card, get_visit_cards, create_visit_card


class ExchangeState(Enum):
    VISIT_CARD_AGREE = 1
    VISIT_CARD_DETAILS = 2
    HANDLE_VISIT_CARDS = 3


def start_exchange(update, context):
    user_id = update.message.from_user.id
    card = get_visit_card(user_id)
    if card:
        keyboard = [
            [
                InlineKeyboardButton('Обновить', callback_data='update'),
                InlineKeyboardButton('Использовать текущую', callback_data='use_current'),
            ],
            [InlineKeyboardButton('В главное меню', callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = textwrap.dedent(f'''
            Ваша визитка:
            Имя: {card['first_name']} {card['last_name']}
            Должность: {card['job_title']}
            Телефон: {card['phone']}\n
            Хотите обновить ее или использовать текущую?
            ''')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup
        )
    else:
        keyboard = [
            [
                InlineKeyboardButton('Да', callback_data='yes'),
                InlineKeyboardButton('Нет', callback_data='no'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Вы хотите обменяться визитками?',
            reply_markup=reply_markup
        )
    return ExchangeState.VISIT_CARD_AGREE


def handle_exchange_response(update, context):
    user_id = update.effective_user.id
    query = update.callback_query
    if query.data == 'yes' or query.data == 'update':
        keyboard = [[InlineKeyboardButton('В главное меню', callback_data='back_to_menu')]]
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Пожалуйста, введите свои данные в следующем формате:\n\n'
                 'Имя Фамилия\n'
                 'Должность\n'
                 'Телефон',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return ExchangeState.VISIT_CARD_DETAILS
    elif query.data == 'use_current':
        all_cards = get_visit_cards(user_id)
        context.user_data['cards'] = all_cards
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Ваша текущая визитка будет использована.'
        )
        return send_cards(update, context)
    else:
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='ОК, в любое время вы можете начать обмен визитками.'
        )
        return send_main_menu(update, context)


def handle_details(update, context):
    details = update.message.text.split('\n')
    user_id = update.message.from_user.id

    if len(details) < 3:
        update.message.reply_text('Введите все данные в нужном формате, пожалуйста.')
        return ExchangeState.VISIT_CARD_DETAILS

    card = create_visit_card(telegram_id=user_id,
                             first_name=details[0].split()[0],
                             last_name=details[0].split()[1],
                             job_title=details[1],
                             phone=details[2])

    all_cards = get_visit_cards(user_id)

    context.user_data['cards'] = all_cards

    update.message.reply_text('Ваша визитка сохранена.')

    return send_cards(update, context)


def get_cards_text(chunked_cards, chunk):
    if len(chunked_cards) == 0:
        text = 'Карты не найдены.'
    else:
        text = ''
        for card in chunked_cards[chunk]:
            text += textwrap.dedent(f'''
                Имя: {card['first_name']} {card['last_name']}
                Должность: {card['job_title']}
                Телефон: {card['phone']}\n''')
    return text


def send_cards(update, context):
    chunk_size = 5
    chunk = 0
    cards = context.user_data['cards']
    chunked_cards = list(chunked(cards, chunk_size))

    reply_markup = get_arrows_keyboard(chunked_cards, chunk)
    text = get_cards_text(chunked_cards, chunk)

    context.user_data['chunk'] = chunk
    context.user_data['chunked_cards'] = chunked_cards
    query = update.callback_query
    if query:
        message_id = query.message.message_id
        context.bot.delete_message(update.effective_chat.id, message_id)
    context.bot.send_message(
        update.effective_chat.id,
        text=text,
        reply_markup=reply_markup
    )

    return ExchangeState.HANDLE_VISIT_CARDS


def handle_visit_cards(update, context):
    query = update.callback_query
    if query.data == "⬅️":
        context.user_data['chunk'] -= 1
    elif query.data == "➡️":
        context.user_data['chunk'] += 1

    chunked_cards = context.user_data['chunked_cards']
    chunk = context.user_data['chunk']

    reply_markup = get_arrows_keyboard(chunked_cards, chunk)
    text = get_cards_text(chunked_cards, chunk)

    query.edit_message_text(
        text=text,
        reply_markup=reply_markup
    )

    return ExchangeState.HANDLE_VISIT_CARDS
