import textwrap
from enum import Enum

from more_itertools import chunked
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .keyboards import get_questions_keyboard
from .main_menu import send_main_menu
from backend.utils import get_current_event, create_question, get_to_speaker_questions, get_user, get_from_guest_questions


class QuestionsState(Enum):
    SAVE_QUESTION = 1
    CHOOSE_ASKED_QUESTIONS = 2
    ASKED_QUESTIONS = 3


def handle_ask_question(update, context):
    current_event = get_current_event()
    if not current_event:
        update.message.reply_text(
            text='Программы на сегодня нет, либо событие ещё не началось( Попробуйте позже'
        )
        return send_main_menu(update, context)
    context.user_data['current_event'] = current_event
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Назад', callback_data='back_to_menu')]])
    update.message.reply_text(
        text=f'''Задать вопрос к событию {current_event['title']}. Введите свой вопрос.''',
        reply_markup=reply_markup
    )

    return QuestionsState.SAVE_QUESTION


def handle_save_question(update, context):
    content = update.message.text
    user_id = update.message.from_user.id
    event = context.user_data['current_event']
    question = create_question(user_id, event['title'], content)

    update.message.reply_text(
        'Ваш вопрос был отправлен. Спасибо за участие!'
    )

    return send_main_menu(update, context)


def get_asked_questions_text(chunked_questions, chunk):
    if len(chunked_questions) == 0:
        text = 'Вопросы не найдены.'
    else:
        text = ''
        for question in chunked_questions[chunk]:
            text += textwrap.dedent(f'''
                Вопрос: {question['content']}\n
            ''')
    return text


def start_questions(update, context):
    user_id = update.message.from_user.id
    user = get_user(user_id)
    if not user['is_speaker']:
        questions = get_from_guest_questions(user_id)
        return send_questions(update, context, questions)

    keyboard = [[InlineKeyboardButton('Заданные мной вопросы', callback_data='i_asked_questions'),
                 InlineKeyboardButton('Заданные мне вопросы', callback_data='asked_to_me_questions')],
                [InlineKeyboardButton('В главное меню', callback_data='back_to_menu')]]

    update.message.reply_text(
        text='Выберите какие вопросы вы хотите просмотреть.',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return QuestionsState.CHOOSE_ASKED_QUESTIONS


def send_questions_i_asked(update, context):
    user_id = update.effective_user.id
    questions = get_from_guest_questions(user_id)
    return send_questions(update, context, questions)


def send_questions_asked_to_me(update, context):
    user_id = update.effective_user.id
    questions = get_to_speaker_questions(user_id)
    return send_questions(update, context, questions)


def send_questions(update, context, questions):
    chunk_size = 5
    chunk = 0
    chunked_questions = list(chunked(questions, chunk_size))

    reply_markup = get_questions_keyboard(chunked_questions, chunk)
    text = get_asked_questions_text(chunked_questions, chunk)

    context.user_data['chunk'] = chunk
    context.user_data['chunked_questions'] = chunked_questions
    query = update.callback_query
    if query:
        message_id = query.message.message_id
        context.bot.delete_message(update.effective_chat.id, message_id)
    context.bot.send_message(
        update.effective_chat.id,
        text=text,
        reply_markup=reply_markup
    )

    return QuestionsState.ASKED_QUESTIONS


def handle_asked_questions(update, context):
    query = update.callback_query
    if query.data == "⬅️":
        context.user_data['chunk'] -= 1
    elif query.data == "➡️":
        context.user_data['chunk'] += 1

    chunked_questions = context.user_data['chunked_questions']
    chunk = context.user_data['chunk']

    reply_markup = get_questions_keyboard(chunked_questions, chunk)
    text = get_asked_questions_text(chunked_questions, chunk)

    query.edit_message_text(
        text=text,
        reply_markup=reply_markup
    )

    return QuestionsState.ASKED_QUESTIONS


# from django.utils import timezone
#
# from backend.models import Question, User, Event
#
# QUESTION_AGREE, CHOOSE_SPEAKER, ASK_QUESTION = range(3)
#
#
# def start_question(update, context):
#     user = User.objects.filter(telegram_id=str(update.effective_user.id)).first()
#     if not user:
#         context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text="Сначала зарегистрируйтесь, чтобы задать вопрос!"
#         )
#         return ConversationHandler.END
#     else:
#         context.user_data['user_profile'] = user
#         today = timezone.localdate()
#         today_events = Event.objects.filter(date=today)
#         speakers = {event.speaker.id: event.speaker.name for event in today_events}
#         context.user_data['speakers'] = speakers
#
#         keyboard = [[InlineKeyboardButton(speaker, callback_data=id)] for id, speaker in speakers.items()]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         context.bot.send_message(chat_id=update.effective_chat.id,
#                                  text="Выберите спикера, которому хотите задать вопрос:",
#                                  reply_markup=reply_markup)
#         return CHOOSE_SPEAKER
#
#
# def handle_speaker_choice(update, context):
#     update.callback_query.data = int(update.callback_query.data)
#     speaker_id = update.callback_query.data  # convert string to integer
#     context.user_data['chosen_speaker'] = context.user_data['speakers'][speaker_id]
#
#     query = update.callback_query
#     speaker_id = query.data
#     context.user_data['chosen_speaker'] = context.user_data['speakers'][speaker_id]
#     context.bot.edit_message_text(chat_id=query.message.chat_id,
#                                   message_id=query.message.message_id,
#                                   text=f"Вы выбрали спикера {context.user_data['chosen_speaker']}. Введите свой вопрос.")
#     return ASK_QUESTION
#
#
# def handle_question(update, context):
#     user = context.user_data['user_profile']
#     speaker_name = context.user_data['chosen_speaker']
#     speaker = User.objects.get(name=speaker_name)
#     today = timezone.localdate()
#     event = Event.objects.get(date=today, speaker=speaker)
#
#     question_text = update.message.text
#     question = Question(guest=user, event=event, content=question_text)
#     question.save()
#
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                              text="Ваш вопрос был сохранен. Спасибо за участие!")
#     return ConversationHandler.END
#
#
# def main():
#     env = Env()
#     env.read_env()
#
#     bot_token = env('TELEGRAM_TOKEN')
#     updater = Updater(token=bot_token, use_context=True)
#     dispatcher = updater.dispatcher
#
#     question_handler = ConversationHandler(
#         entry_points=[CommandHandler('ask_question', start_question)],
#         states={
#             CHOOSE_SPEAKER: [
#                 CallbackQueryHandler(
#                     handle_speaker_choice
#                 ),
#             ],
#             ASK_QUESTION: [
#                 MessageHandler(
#                     Filters.text,
#                     handle_question,
#                 )
#             ],
#         },
#         fallbacks=[
#             CommandHandler('start', start_question)
#         ]
#     )
#
#     dispatcher.add_handler(question_handler)
#
#     updater.start_polling()
#     updater.idle()
#
#
# if __name__ == '__main__':
#     main()
