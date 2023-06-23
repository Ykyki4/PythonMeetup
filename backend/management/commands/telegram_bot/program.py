import time
from enum import Enum

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

from .keyboards import get_keyboard, main_menu_buttons
from backend.utils import get_events, get_event


class ProgramState(Enum):
    SELECTED_PROGRAM = 1
    HANDLED_PROGRAM = 2
    SELECTED_DATA = 3
    HANDLED_DATE = 4
    HANDLED_SPEAKER = 5
    ISSUED_MAIN_MENU = 6


def handle_program(update, context):
    query = update.callback_query
    events = get_events()
    events_titles = [event['title'] for event in events]
    events_titles.append('Назад')
    text = 'Выберите интересующее событие: '
    if query:
        message_id = query.message.message_id
        context.bot.delete_message(update.effective_chat.id, message_id)
        context.bot.send_message(
            update.effective_chat.id,
            text=text,
            reply_markup=get_keyboard(events_titles)
        )
    else:
        update.message.reply_text(
            text=text,
            reply_markup=get_keyboard(events_titles),
        )

    return ProgramState.SELECTED_PROGRAM


def handle_selected_program(update, context):
    query = update.callback_query
    titled_text = 'Загружаю мероприятие'
    keyboard = [
        [
            InlineKeyboardButton('Дата и время', callback_data='date'),
            InlineKeyboardButton('Спикер', callback_data='speaker'),
            InlineKeyboardButton('Назад', callback_data='back_to_programs')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if query:
        event = context.user_data['event']
        query.edit_message_text(
            text=event['description'],
            reply_markup=reply_markup,
        )
        return ProgramState.SELECTED_DATA

    else:
        text = update.message.text
        event = get_event(text)

        if event:
            context.user_data['event'] = event
            update.message.reply_text(
                text=titled_text,
                reply_markup=ReplyKeyboardRemove(),
            )
            time.sleep(2)
            update.message.reply_text(
                text=event['description'],
                reply_markup=reply_markup,
            )

            return ProgramState.SELECTED_DATA
        elif text == 'Назад':
            update.message.reply_text(
                text='Выберите один из следующих пунктов: ',
                reply_markup=get_keyboard(list(main_menu_buttons.values())),
            )
            return ProgramState.ISSUED_MAIN_MENU

        else:
            return ProgramState.SELECTED_PROGRAM


def handle_date(update, context):
    query = update.callback_query
    event = context.user_data['event']
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data='back_to_program')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f'Мероприятие {event["title"]} будет проходить '
             f'{event["date"].strftime("%d-%m-%Y")} '
             f'в {event["time"].strftime("%H:%M")}',
        reply_markup=reply_markup
    )
    return ProgramState.HANDLED_DATE


def handle_speaker(update, context):
    query = update.callback_query
    event = context.user_data['event']
    speaker = event['speaker']
    context.user_data['speaker'] = speaker
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data='back_to_program'),
            InlineKeyboardButton('Задать вопрос спикеру', callback_data='ask_speaker')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f'На {event["title"]} будет выступать {speaker["name"]} - профессионал своего дела.\n'
             f'Если у вас есть вопросы, можете задать их спикеру, '
             f'который обязательно ответит на него во время мероприятия',
        reply_markup=reply_markup
    )
    return ProgramState.HANDLED_SPEAKER


