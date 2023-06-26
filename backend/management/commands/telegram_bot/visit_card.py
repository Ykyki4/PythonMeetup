import textwrap
from enum import Enum

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

from backend.utils import get_visit_card, get_visit_cards, create_visit_card


class ExchangeState(Enum):
    VISIT_CARD_AGREE = 1
    VISIT_CARD_DETAILS = 2


def start_exchange(update, context):
    user_id = update.message.from_user.id
    existing_card = get_visit_card(user_id)
    if existing_card:
        keyboard = [
            [
                InlineKeyboardButton('Обновить', callback_data='update'),
                InlineKeyboardButton('Использовать текущую', callback_data='use_current'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='У вас уже есть визитка. Хотите обновить ее или использовать текущую?',
            reply_markup=reply_markup
        )
        return ExchangeState.VISIT_CARD_AGREE
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
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Пожалуйста, введите свои данные в следующем формате:\n\n'
                 'Имя Фамилия\n'
                 'Должность\n'
                 'Телефон'
        )
        return ExchangeState.VISIT_CARD_DETAILS
    elif query.data == 'use_current':
        all_cards = get_visit_cards(user_id)
        all_cards_text = ''
        for card in all_cards:
            all_cards_text += textwrap.dedent(f'''
            Имя: {card['first_name']} {card['last_name']}
            Должность: {card['job_title']}
            Телефон: {card['phone']}\n''')
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Ваша текущая визитка будет использована. Вот все визитки:\n\n' + all_cards_text
        )
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='ОК, в любое время вы можете начать обмен визитками.'
        )
        return ConversationHandler.END


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

    all_cards_text = ''
    for card in all_cards:
        all_cards_text += textwrap.dedent(f'''
        Имя: {card['first_name']} {card['last_name']}
        Должность: {card['job_title']}
        Телефон: {card['phone']}\n''')

    update.message.reply_text('Ваша визитка сохранена. Вот все визитки:\n\n' + all_cards_text)

    return ConversationHandler.END

# def main():
#     env = Env()
#     env.read_env()
#
#     bot_token = env('TELEGRAM_TOKEN')
#     updater = Updater(token=bot_token, use_context=True)
#     dispatcher = updater.dispatcher
#
#     conversation_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', start_exchange)],
#         states={
#             VISIT_CARD_AGREE: [
#                 CallbackQueryHandler(
#                     handle_exchange_response
#                 ),
#             ],
#             VISIT_CARD_DETAILS: [
#                 MessageHandler(
#                     Filters.text,
#                     handle_details,
#                 )
#             ],
#         },
#         fallbacks=[
#             CommandHandler('start', start_exchange)
#         ]
#     )
#
#     dispatcher.add_handler(conversation_handler)
#     updater.start_polling()
#     updater.idle()
#
#
# if __name__ == '__main__':
#     main()
