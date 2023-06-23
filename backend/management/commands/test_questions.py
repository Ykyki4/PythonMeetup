from django.core.management import BaseCommand

from .telegram_bot.questions import main


class Command(BaseCommand):
    help = 'Запуск тестового бота по вопросам'

    def handle(self, *args, **kwargs):
        main()
