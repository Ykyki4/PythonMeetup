from environs import Env
from telegram.ext import Updater, CallbackQueryHandler

from registration import registration_conversation_handler, registration_callback_handler


def main():
    env = Env()
    env.read_env()

    bot_token = env('TELEGRAM_TOKEN')
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(registration_conversation_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(registration_callback_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()