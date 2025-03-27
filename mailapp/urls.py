
from django.urls import path

from mailapp.apps import MailappConfig

from mailapp import views

app_name = MailappConfig.name

urlpatterns = [
    path("", views.IndexTemplateView.as_view(), name="index"),
    path("recipient/", views.RecipientMailListViews.as_view(), name="recipient_list"),
    path("recipient/create/", views.RecipientMailCreateViews.as_view(), name="recipient_create"),
    path("recipient/detail/<int:pk>/", views.RecipientMailDetailViews.as_view(), name="recipient_detail"),
    path("recipient/update/<int:pk>/", views.RecipientMailUpdateViews.as_view(), name="recipient_update"),
    path("recipient/delete/<int:pk>/", views.RecipientMailDeleteViews.as_view(), name="recipient_delete"),
    path("message/create/", views.MailMessageCreateView.as_view(), name="create_message"),
    path("message/detail/<int:pk>/", views.MailMessageDetailView.as_view(), name="mail_message_detail"),
    path("message/update/<int:pk>/", views.MailMessageUpdateView.as_view(), name="mail_update_message"),
    path("message/delete/<int:pk>/", views.MailMessageDeleteView.as_view(), name="mail_delete_message"),
    path("message/list/", views.MailMessageListView.as_view(), name="mail_message_list"),
    path("attempts/", views.MailingAttemptListView.as_view(), name="mailing_attempts"),
    path("mailing/", views.MailingListView.as_view(), name="mailing_list"),
    path("mailing/create/", views.MailingCreateView.as_view(), name="create_mailing"),
    path("mailing/detail/<int:pk>/", views.MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/update/<int:pk>/", views.MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/delete/<int:pk>/", views.MailingDeleteView.as_view(), name="mailing_delete"),
]
