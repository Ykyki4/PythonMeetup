from enum import Enum

from telegram import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup


from .keyboards import main_menu_buttons, get_keyboard
from backend.utils import create_user, get_user


class RegistrationState(Enum):
    PROCESSED_REGISTRATION = 1
    ASKED_NEW_NAME = 2
    ASKED_NAME = 3


def start(update, context):
    user = update.message.from_user
    user_first_name = user['first_name']
    user_last_name = user['last_name']
    user_id = user['id']
    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text(
        text='Здравствуйте. Это официальный бот по поддержке участников 🤖.',
        reply_markup=reply_markup,
    )
    user = get_user(user_id)

    if user:
        update.message.reply_text(
            text='Авторизация пройдена! \nВыберите один из следующих пунктов: ',
            reply_markup=get_keyboard(list(main_menu_buttons.values())),
        )
        return RegistrationState.PROCESSED_REGISTRATION
    else:
        keyboard = [
            [
                InlineKeyboardButton('Да, все верно', callback_data='accept_name'),
                InlineKeyboardButton('Нет, изменить', callback_data='change_name'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if user_last_name:
            update.message.reply_text(
                f'{user_first_name} {user_last_name} - это Ваши имя и фамилия?',
                reply_markup=reply_markup
            )
        else:
            update.message.reply_text(
                f'{user_first_name} - это Ваше имя?',
                reply_markup=reply_markup
            )
        return RegistrationState.ASKED_NAME


def handle_name(update, context):
    query = update.callback_query
    message_id = query.message.message_id
    user_id = update['callback_query']['message']['chat']['id']

    if query.data == 'accept_name':
        user_first_name = update['callback_query']['message']['chat']['first_name']
        user_last_name = update['callback_query']['message']['chat']['last_name']
        if user_last_name:
            user_name = user_first_name + ' ' + user_last_name
        else:
            user_name = user_first_name

        context.bot.delete_message(update.effective_chat.id, message_id)
        message = 'Выберите один из следующих пунктов: '
        reply_markup = get_keyboard(list(main_menu_buttons.values()))
        context.bot.sendMessage(update.effective_chat.id, text=message, reply_markup=reply_markup)
        create_user(user_id, user_name)
        return RegistrationState.PROCESSED_REGISTRATION

    else:
        query.edit_message_text(text='Введите, пожалуйста, ваше имя и фамилию')
        return RegistrationState.ASKED_NEW_NAME


def handle_new_name(update, context):
    user_name = update.message.text
    user_id = update.message.from_user.id
    reply_markup = get_keyboard(list(main_menu_buttons.values()))
    update.message.reply_text(
        text='Выберите один из следующих пунктов: ',
        reply_markup=reply_markup
    )
    create_user(user_id, user_name)
    return RegistrationState.PROCESSED_REGISTRATION
