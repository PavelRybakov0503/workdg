from django.core.management.base import BaseCommand

from mailapp.services import MailingService
from mailapp.models import Mailing


class Command(BaseCommand):
    help = "Для запуска рассылки введите ID рассылки"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int)
        parser.add_argument("--status", choices=["Создана", "Запущена", "Завершена"], default="Создана")

        # optional argument
        parser.add_argument("--frequency", choices=["раз в минуту", "раз в день", "раз в неделю", "раз в месяц"],
                            default="раз в день")

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        status = options["status"]
        frequency = options["frequency"]

        mailing = Mailing.objects.get(id=mailing_id)
        mailing.status = status
        mailing.frequency = frequency
        mailing.save()

        MailingService.start_mailing(mailing)

        self.stdout.write(self.style.SUCCESS(f"Mailing with ID {mailing_id} has been started"))
