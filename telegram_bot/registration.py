from enum import Enum
from functools import partial

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from keyboards import main_menu_buttons


class State(Enum):
    PROCESSED_REGISTRATION = 1
    ASKED_NEW_NAME = 2
    ASKED_NAME = 3


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
    # TODO Здесь делаем запрос к БД
    # TODO Здесь присваиваем пользователю роль
    user_role = ''

    if user_role:
        update.message.reply_text(
            text='Регистрация пройдена! \nВыберите один из следующих пунктов: ',
            reply_markup=get_keyboard(list(main_menu_buttons.values())),
        )
        return State.PROCESSED_REGISTRATION
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
        return State.ASKED_NAME


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
        # TODO Здесь сохраняем пользователя в БД
        return State.PROCESSED_REGISTRATION

    else:
        query.edit_message_text(text='Введите, пожалуйста, ваше имя и фамилию')
        return State.ASKED_NEW_NAME


def handle_new_name(update, context):
    user_name = update.message.text
    reply_markup = get_keyboard(list(main_menu_buttons.values()))
    update.message.reply_text(
        text='Выберите один из следующих пунктов: ',
        reply_markup=reply_markup
    )
    # TODO Здесь сохраняем пользователя в БД
    return State.PROCESSED_REGISTRATION


def handle_main_menu(update, context):
    pass


registration_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        # State.PROCESSED_REGISTRATION: [
        #     MessageHandler(
        #         Filters.regex(''.join(menu_selection_buttons)),
        #         handle_main_menu
        #     )
        # ],
        State.ASKED_NAME: [
            CallbackQueryHandler(
                handle_name
            ),
        ],
        State.ASKED_NEW_NAME: [
            MessageHandler(
                Filters.text,
                handle_new_name,
            )
        ],
    },
    fallbacks=[
        CommandHandler('start', start)
    ]
)