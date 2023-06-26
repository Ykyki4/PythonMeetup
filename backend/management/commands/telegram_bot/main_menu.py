from enum import Enum

from .keyboards import get_keyboard, main_menu_buttons


class MainMenuState(Enum):
    HANDLE_MAIN_MENU = 1


def send_main_menu(update, context):
    query = update.callback_query
    if query:
        context.bot.delete_message(update.effective_chat.id, query.message.message_id)
        main_menu_message = context.bot.send_message(
            update.effective_chat.id,
            text='Выберите один из следующих пунктов: ',
            reply_markup=get_keyboard(list(main_menu_buttons.values()), 3),
        )
    else:
        main_menu_message = update.message.reply_text(
            text='Выберите один из следующих пунктов: ',
            reply_markup=get_keyboard(list(main_menu_buttons.values()), 3),
        )
    context.user_data['main_menu_message_id'] = main_menu_message.message_id
    return MainMenuState.HANDLE_MAIN_MENU
