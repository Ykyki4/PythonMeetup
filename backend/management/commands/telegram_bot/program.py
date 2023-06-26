import textwrap
import time
from enum import Enum

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

from .keyboards import get_keyboard
from backend.utils import get_today_meetup, get_event
from .main_menu import send_main_menu


class ProgramState(Enum):
    SELECTED_PROGRAM = 1
    HANDLED_PROGRAM = 2
    SELECTED_DATA = 3
    HANDLED_DATE = 4
    HANDLED_SPEAKER = 5
    SAVE_QUESTION = 6


def handle_program(update, context):
    query = update.callback_query
    meetup = get_today_meetup()
    if not meetup:
        update.message.reply_text(
            text='Программы на сегодня нет( Попробуйте позже',
        )
        return send_main_menu(update, context)

    events_titles = [event['title'] for event in meetup['events']]
    events_titles.append('Назад')

    text = textwrap.dedent(f'''
        Сегодняшняя программа: {meetup['title']}\n    
        Выберите интересующее событие: 
    ''')
    if query:
        message_id = query.message.message_id
        context.bot.delete_message(update.effective_chat.id, message_id)
        message = context.bot.send_message(
            update.effective_chat.id,
            text=text,
            reply_markup=get_keyboard(events_titles)
        )
    else:
        program_title_message = update.message.reply_text(
            text=text,
            reply_markup=get_keyboard(events_titles),
        )
    context.user_data['program_title_message_id'] = program_title_message.message_id
    return ProgramState.SELECTED_PROGRAM


def handle_selected_program(update, context):
    query = update.callback_query
    program_title_message_id = context.user_data['program_title_message_id']
    keyboard = [
        [
            InlineKeyboardButton('Время', callback_data='time'),
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
            context.bot.delete_message(update.effective_chat.id, program_title_message_id)
            update.message.reply_text(
                text=event['description'],
                reply_markup=reply_markup,
            )

            return ProgramState.SELECTED_DATA
        elif text == 'Назад':
            return send_main_menu(update, context)

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
