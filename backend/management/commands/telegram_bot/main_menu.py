from enum import Enum

from .keyboards import get_keyboard, main_menu_buttons


class MainMenuState(Enum):
    HandleMainMenu = 1


def send_main_menu(update, context):
    query = update.callback_query
    if query:
        context.bot.delete_message(update.effective_chat.id, query.message.message_id)
        context.bot.send_message(
            update.effective_chat.id,
            text='Выберите один из следующих пунктов: ',
            reply_markup=get_keyboard(list(main_menu_buttons.values())),
        )
    else:
        update.message.reply_text(
            text='Выберите один из следующих пунктов: ',
            reply_markup=get_keyboard(list(main_menu_buttons.values())),
        )
    return MainMenuState.HandleMainMenu
