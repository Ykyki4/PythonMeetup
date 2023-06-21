from django.core.management import BaseCommand

from .telegram_bot.main import main


class Command(BaseCommand):
    help = 'Starts telegram bot'

    def handle(self, *args, **options):
        main()