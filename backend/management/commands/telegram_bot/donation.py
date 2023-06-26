from enum import Enum

import telegram
from environs import Env

from telegram import LabeledPrice

from .keyboards import donation_buttons, get_keyboard
from .main_menu import send_main_menu


class DonationState(Enum):
    HANDLED_SUM = 1
    PROCESSED_PAYMENT = 2
    HANDLED_CUSTOM_SUM = 3
    SUCCEED_PAYMENT = 4


def handle_donation(update, context):
    buttons = list(donation_buttons.values())
    buttons.append('Назад')
    message = update.message.reply_text(
        text='Вы можете выбрать сумму поддержки либо написать свою.\n'
             'Сумма должна быть от 10 рублей.',
        reply_markup=get_keyboard(buttons, 3),
    )
    context.user_data['payment_title_message_id'] = message.message_id
    return DonationState.HANDLED_SUM


def handle_pay_process(update, context):
    chat_id = update.message.chat_id
    message_id = context.user_data['payment_title_message_id']
    text = update.message.text
    if text == 'Назад':
        return send_main_menu(update, context)
    else:
        try:
            price = int(text.replace(' рублей', ''))
            title = 'Поддержка Python Meetup'
            description = 'Поддержка развития проекта Python Meetup'
            payload = "Custom-Payload"
            env = Env()
            env.read_env()
            provider_token = env('PAYMENTS_PROVIDER_TOKEN')
            currency = 'rub'
            prices = [LabeledPrice('Поддержка Python Meetup', price * 100)]
            context.bot.send_invoice(
                chat_id, title, description, payload, provider_token, currency, prices
            )
            context.bot.delete_message(update.effective_chat.id, message_id)
            return DonationState.PROCESSED_PAYMENT

        except ValueError:
            context.bot.send_message(
                update.effective_chat.id,
                text='Пожалуйста, введите сумму от 10 рублей ещё раз, либо используйте кнопки',
                reply_markup=get_keyboard(list(donation_buttons.values()), 3),
            )
            return DonationState.HANDLED_CUSTOM_SUM
        except telegram.error.BadRequest as exception:
            if exception.message == 'Currency_total_amount_invalid':
                context.bot.send_message(
                    update.effective_chat.id,
                    text='Введенная сумма должна быть не меньше 10 рублей.\n'
                         'Пожалуйста, повторите ввод или используйте кнопки',
                    reply_markup=get_keyboard(list(donation_buttons.values()), 3),
                )
            else:
                pass
            return DonationState.HANDLED_CUSTOM_SUM


def handle_pre_checkout_callback(update, context):
    query = update.pre_checkout_query
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message='Что-то пошло не так.'
                                             ' Если проблема повторяется, перезапустите бота')
    else:
        query.answer(ok=True)
        return DonationState.SUCCEED_PAYMENT


def handle_successful_payment_callback(update, context):
    update.message.reply_text('Спасибо за поддержку!')
    return send_main_menu(update, context)
