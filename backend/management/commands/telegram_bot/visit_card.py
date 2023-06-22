from environs import Env
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

from backend.models import VisitCard, User

VISIT_CARD_AGREE, VISIT_CARD_DETAILS = range(2)


def start_exchange(update, context):
    user = User.objects.filter(telegram_id=str(update.effective_user.id)).first()
    if not user:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Сначала зарегистрируйтесь, чтобы отправлять визитки!"
        )
        return ConversationHandler.END
    else:
        context.user_data['user_profile'] = user
        existing_card = VisitCard.objects.filter(owner=user).first()
        if existing_card:
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("Обновить", callback_data='update'),
                    InlineKeyboardButton("Использовать текущую", callback_data='use_current'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                      text="У вас уже есть визитка. Хотите обновить ее или использовать текущую?",
                                      reply_markup=reply_markup)
            return VISIT_CARD_AGREE
        else:
            context.user_data['user_profile'] = user
            keyboard = [
                [
                    InlineKeyboardButton("Да", callback_data='yes'),
                    InlineKeyboardButton("Нет", callback_data='no'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Вы хотите обменяться визитками?",
                                     reply_markup=reply_markup)
        return VISIT_CARD_AGREE


def handle_exchange_response(update, context):
    query = update.callback_query
    if query.data == 'yes' or query.data == 'update':
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="Пожалуйста, введите свои данные в следующем формате:\n\n"
                                           "Имя Фамилия\n"
                                           "Должность\n"
                                           "Телефон")
        return VISIT_CARD_DETAILS
    elif query.data == 'use_current':
        all_cards = VisitCard.objects.all()
        all_cards_text = ""
        for card in all_cards:
            all_cards_text += f"Имя: {card.first_name} {card.last_name}\nДолжность: {card.job_title}\nТелефон: {card.phone}\n\n"
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="Ваша текущая визитка будет использована. Вот все визитки:\n\n" + all_cards_text)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="ОК, в любое время вы можете начать обмен визитками.")
        return ConversationHandler.END


def handle_details(update, context):
    details = update.message.text.split('\n')

    if len(details) < 3:
        update.message.reply_text('Введите все данные в нужном формате, пожалуйста.')
        return VISIT_CARD_DETAILS

    card = VisitCard(owner=context.user_data['user_profile'],
                     first_name=details[0].split()[0],
                     last_name=details[0].split()[1],
                     job_title=details[1],
                     phone=details[2])
    card.save()

    all_cards = VisitCard.objects.all()

    all_cards_text = ""
    for card in all_cards:
        all_cards_text += f"Имя: {card.first_name} {card.last_name}\nДолжность: {card.job_title}\nТелефон: {card.phone}\n\n"

    update.message.reply_text('Ваша визитка сохранена. Вот все визитки:\n\n' + all_cards_text)

    return ConversationHandler.END


def main():
    env = Env()
    env.read_env()

    bot_token = env('TELEGRAM_TOKEN')
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_exchange)],
        states={
            VISIT_CARD_AGREE: [
                CallbackQueryHandler(
                    handle_exchange_response
                ),
            ],
            VISIT_CARD_DETAILS: [
                MessageHandler(
                    Filters.text,
                    handle_details,
                )
            ],
        },
        fallbacks=[
            CommandHandler('start', start_exchange)
        ]
    )

    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
