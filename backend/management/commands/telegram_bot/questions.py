from environs import Env
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

from django.utils import timezone

from backend.models import Question, User, Event

QUESTION_AGREE, CHOOSE_SPEAKER, ASK_QUESTION = range(3)


def start_question(update, context):
    user = User.objects.filter(telegram_id=str(update.effective_user.id)).first()
    if not user:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Сначала зарегистрируйтесь, чтобы задать вопрос!"
        )
        return ConversationHandler.END
    else:
        context.user_data['user_profile'] = user
        today = timezone.localdate()
        today_events = Event.objects.filter(date=today)
        speakers = {event.speaker.id: event.speaker.name for event in today_events}
        context.user_data['speakers'] = speakers

        keyboard = [[InlineKeyboardButton(speaker, callback_data=id)] for id, speaker in speakers.items()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Выберите спикера, которому хотите задать вопрос:",
                                 reply_markup=reply_markup)
        return CHOOSE_SPEAKER


def handle_speaker_choice(update, context):
    update.callback_query.data = int(update.callback_query.data)
    speaker_id = update.callback_query.data  # convert string to integer
    context.user_data['chosen_speaker'] = context.user_data['speakers'][speaker_id]

    query = update.callback_query
    speaker_id = query.data
    context.user_data['chosen_speaker'] = context.user_data['speakers'][speaker_id]
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=f"Вы выбрали спикера {context.user_data['chosen_speaker']}. Введите свой вопрос.")
    return ASK_QUESTION


def handle_question(update, context):
    user = context.user_data['user_profile']
    speaker_name = context.user_data['chosen_speaker']
    speaker = User.objects.get(name=speaker_name)
    today = timezone.localdate()
    event = Event.objects.get(date=today, speaker=speaker)

    question_text = update.message.text
    question = Question(guest=user, event=event, content=question_text)
    question.save()

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Ваш вопрос был сохранен. Спасибо за участие!")
    return ConversationHandler.END


def main():
    env = Env()
    env.read_env()

    bot_token = env('TELEGRAM_TOKEN')
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    question_handler = ConversationHandler(
        entry_points=[CommandHandler('ask_question', start_question)],
        states={
            CHOOSE_SPEAKER: [
                CallbackQueryHandler(
                    handle_speaker_choice
                ),
            ],
            ASK_QUESTION: [
                MessageHandler(
                    Filters.text,
                    handle_question,
                )
            ],
        },
        fallbacks=[
            CommandHandler('start', start_question)
        ]
    )

    dispatcher.add_handler(question_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()