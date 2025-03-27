import secrets

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


class UserService:

    @staticmethod
    def send_verification_email(user, host):
        verification_token = secrets.token_urlsafe(16)
        user.verification_token = verification_token
        user.save()
        url = f'http://{host}/users/verify/{verification_token}/'
        subject = 'Подтверждение аккаунта'
        message = f'Пожалуйста, перейдите по ссылке, чтобы подтвердить ваш аккаунт: {url}'
        send_mail(subject, message, EMAIL_HOST_USER, [user.email])

    @staticmethod
    def reset_password(user):
        reset_token = secrets.token_urlsafe(16)
        user.reset_token = reset_token
        user.save()
        host = user.request.get_host()
        url = f'http://{host}/users/reset/{reset_token}/'
        subject = 'Восстановление пароля'
        message = f'Пожалуйста, перейдите по ссылке, чтобы восстановить ваш пароль: {url}'
        send_mail(subject, message, EMAIL_HOST_USER, [user.email])
