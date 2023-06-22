from django.core.management import BaseCommand

from .telegram_bot.visit_card import main


class Command(BaseCommand):
    help = 'Запуск тестового бота по визиткам'

    def handle(self, *args, **kwargs):
        main()
