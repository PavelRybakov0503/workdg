from smtplib import SMTPException

from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER

from .models import MailingAttempt


class MailingService:
    @staticmethod
    def start_mailing(mailing):
        if mailing.start_time is None:
            mailing.start_time = timezone.now()
        mailing.end_time = timezone.now()
        mailing.save()

        subject = mailing.message.subject
        message = mailing.message.body
        recipients = [recipient.email for recipient in mailing.recipients.all()]

        for recipient in recipients:
            try:
                # send_mail возвращает количество успешно отправленных писем
                success = send_mail(
                    subject,
                    message,
                    EMAIL_HOST_USER,
                    [
                        recipient,
                    ],
                    fail_silently=False,
                )
                mailing.status = "Запущена"
                mailing.save()

                # Создаем запись попытки отправки
                mailing_attempt = MailingAttempt.objects.create(
                    status=MailingAttempt.SUCCESSFULLY if success > 0 else MailingAttempt.UNSUCCESSFULLY,
                    mail_server_response="Успешно" if success > 0 else "Ошибка",
                    mailing=mailing,
                )
                mailing_attempt.save()

            except SMTPException as e:
                # Обработка ошибок SMTP
                mailing_attempt = MailingAttempt.objects.create(
                    status=MailingAttempt.UNSUCCESSFULLY, mail_server_response=str(e), mailing=mailing
                )
                mailing_attempt.save()

            except Exception as e:
                # Обработка других неожиданных ошибок
                mailing_attempt = MailingAttempt.objects.create(
                    status=MailingAttempt.UNSUCCESSFULLY,
                    mail_server_response=f"Неожиданная ошибка: {str(e)}",
                    mailing=mailing,
                )
                mailing_attempt.save()

    @staticmethod
    def stop_mailing(mailing):
        mailing.status = "Завершена"
        mailing.save()
