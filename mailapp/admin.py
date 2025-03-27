from django.contrib import admin

from mailapp.models import Mailing, MailingAttempt, MailMessage, RecipientMail


@admin.register(RecipientMail)
class RecipientMailAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "comment")
    search_fields = ("full_name", "comment")
    list_filter = ("full_name",)
    ordering = ("full_name",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "start_time", "end_time")
    search_fields = ("status",)
    list_filter = ("status", "start_time", "end_time")
    ordering = ("-start_time",)


@admin.register(MailMessage)
class MailMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject")
    search_fields = ("subject",)
    list_filter = ("subject",)
    ordering = ("subject",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "date_mailing", "status", "mail_server_response", "mailing")
