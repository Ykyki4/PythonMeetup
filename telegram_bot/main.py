from enum import Enum

from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from registration import start, handle_name, handle_new_name, RegistrationState


def main():
    env = Env()
    env.read_env()

    bot_token = env('TELEGRAM_TOKEN')
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            # RegistrationState.PROCESSED_REGISTRATION: [
            #     MessageHandler(
            #         Filters.regex(''.join(menu_selection_buttons)),
            #         handle_main_menu
            #     )
            # ],
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