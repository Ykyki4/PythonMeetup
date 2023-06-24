from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, \
    PreCheckoutQueryHandler

from backend.management.commands.telegram_bot.donation import handle_donation, DonationState, handle_pay_process, \
    handle_pre_checkout_callback, handle_successful_payment_callback
from .main_menu import MainMenuState, send_main_menu
from .visit_card import start_exchange, ExchangeState, handle_exchange_response, handle_details
from .keyboards import main_menu_buttons
from .registration import start, handle_name, handle_new_name, RegistrationState
from .program import ProgramState, handle_program, handle_selected_program, handle_date, \
    handle_speaker
from .questions import handle_ask_question, handle_save_question, QuestionsState, start_asked_questions, \
    handle_asked_questions


def main():
    env = Env()
    env.read_env()
    bot_token = env('TELEGRAM_TOKEN')
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        per_chat=False,
        entry_points=[CommandHandler('start', start)],
        states={
            MainMenuState.HANDLE_MAIN_MENU: [
                MessageHandler(
                    Filters.regex(''.join(main_menu_buttons['program_button'])),
                    handle_program
                ),
                MessageHandler(
                    Filters.regex(''.join(main_menu_buttons['cards_exchange_button'])),
                    start_exchange
                ),
                MessageHandler(
                    Filters.regex(''.join(main_menu_buttons['ask_question_button'])),
                    handle_ask_question,
                ),
                MessageHandler(
                    Filters.regex(''.join(main_menu_buttons['asked_questions_button'])),
                    start_asked_questions,
                ),
                MessageHandler(
                    Filters.regex(''.join(main_menu_buttons['donation_button'])),
                    handle_donation,
                ),
            ],
            RegistrationState.ASKED_NAME: [
                CallbackQueryHandler(
                    handle_name
                ),
            ],
            RegistrationState.ASKED_NEW_NAME: [
                MessageHandler(
                    Filters.text,
                    handle_new_name,
                )
            ],
            ProgramState.SELECTED_PROGRAM: [
                MessageHandler(
                    Filters.text,
                    handle_selected_program
                ),
            ],
            ProgramState.SELECTED_DATA: [
                CallbackQueryHandler(
                    handle_date,
                    pattern='time'
                ),
                CallbackQueryHandler(
                    handle_speaker,
                    pattern='speaker'
                ),
                CallbackQueryHandler(
                    handle_program,
                    pattern='^back_to_programs$'
                ),
            ],
            ProgramState.HANDLED_DATE: [
                CallbackQueryHandler(
                    handle_selected_program,
                    pattern='^back_to_program$'
                ),
            ],
            ProgramState.HANDLED_SPEAKER: [
                CallbackQueryHandler(
                    handle_selected_program,
                    pattern='^back_to_program$'
                ),
            ],
            QuestionsState.SAVE_QUESTION: [
                CallbackQueryHandler(
                    send_main_menu,
                    pattern='^back_to_menu$'
                ),
                MessageHandler(
                    Filters.text,
                    handle_save_question,
                ),
            ],
            QuestionsState.ASKED_QUESTIONS: [
                CallbackQueryHandler(
                    send_main_menu,
                    pattern='^back_to_menu$'
                ),
                CallbackQueryHandler(
                    handle_asked_questions
                )
            ],
            ExchangeState.VISIT_CARD_AGREE: [
                CallbackQueryHandler(
                    handle_exchange_response
                ),
            ],
            ExchangeState.VISIT_CARD_DETAILS: [
                MessageHandler(
                    Filters.text,
                    handle_details,
                )
            ],
            DonationState.HANDLED_SUM: [
                MessageHandler(
                    Filters.text,
                    handle_pay_process,
                )
            ],
            DonationState.PROCESSED_PAYMENT: [
                PreCheckoutQueryHandler(
                    handle_pre_checkout_callback,
                )
            ],
            DonationState.HANDLED_CUSTOM_SUM: [
                MessageHandler(
                    Filters.text,
                    handle_pay_process,
                )
            ],
            DonationState.SUCCEED_PAYMENT: [
                MessageHandler(
                    Filters.all,
                    handle_successful_payment_callback,
                )
            ]
        },
        fallbacks=[
            CommandHandler('start', start)
        ]
    )

    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()