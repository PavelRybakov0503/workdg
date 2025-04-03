from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import MailingForm, MailMessageForm, RecipientForm
from .models import Mailing, MailingAttempt, MailMessage, RecipientMail
from .services import MailingService


@method_decorator(cache_page(60 * 5), name="dispatch")  # Cache for 5 minutes
class IndexTemplateView(TemplateView):
    template_name = "mailapp/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm("mailapp.can_view_mailing"):
            context["count_mailing"] = Mailing.objects.all().count()
            context["count_active_mailing"] = Mailing.objects.filter(status="Запущена").count()
            context["count_unique_recipients"] = RecipientMail.objects.distinct().count()
            return context
        else:
            context["count_mailing"] = Mailing.objects.filter(owner=self.request.user).count()
            context["count_active_mailing"] = Mailing.objects.filter(
                status="Запущена", owner=self.request.user
            ).count()
            context["count_unique_recipients"] = (
                RecipientMail.objects.filter(owner=self.request.user).distinct().count()
            )
            return context


class RecipientMailListViews(LoginRequiredMixin, ListView):
    model = RecipientMail
    template_name = "mailapp/recipient_mail_list.html"
    context_object_name = "recipients"
    paginate_by = 10
    ordering = ["full_name"]

    def get_queryset(self):
        cached_recipients = cache.get("recipients")
        if cached_recipients:
            return cached_recipients
        # Если кэша нет, получаем объекты из базы и кешируем их
        recipients = RecipientMail.objects.all()
        cache.set("recipients", recipients, 60 * 5)  # Кэшируем на 5 минут
        user = self.request.user
        if user.has_perm("mailapp.can_view_recipient_mail"):
            return RecipientMail.objects.all()
        return RecipientMail.objects.filter(owner=user)


@method_decorator(cache_page(60 * 5), name="dispatch")  # Cache for 5 minutes
class RecipientMailDetailViews(LoginRequiredMixin, DetailView):
    model = RecipientMail
    template_name = "mailapp/recipient_mail_detail.html"
    context_object_name = "recipient"


class RecipientMailCreateViews(LoginRequiredMixin, CreateView):
    model = RecipientMail
    form_class = RecipientForm
    template_name = "mailapp/recipient_mail_form.html"
    success_url = reverse_lazy("mailapp:recipient_list")

    def form_valid(self, form):
        recipient = form.save(commit=False)
        recipient.owner = self.request.user
        recipient.save()
        return redirect(reverse("mailapp:recipient_detail", kwargs={"pk": recipient.pk}))


class RecipientMailUpdateViews(LoginRequiredMixin, UpdateView):
    model = RecipientMail
    template_name = "mailapp/recipient_mail_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("mailapp:recipient_detail")

    def get_success_url(self):
        recipient = self.object
        return reverse_lazy("mailapp:recipient_detail", kwargs={"pk": recipient.pk})


class RecipientMailDeleteViews(LoginRequiredMixin, DeleteView):
    model = RecipientMail
    context_object_name = "recipient"
    template_name = "mailapp/recipient_mail_confirm_delete.html"
    success_url = reverse_lazy("mailapp:recipient_list")


class MailMessageListView(LoginRequiredMixin, ListView):
    model = MailMessage
    template_name = "mailapp/mail_message_list.html"
    context_object_name = "messages"
    paginate_by = 10

    def get_queryset(self):
        cached_messages = cache.get("messages")
        if cached_messages:
            return cached_messages
        # Если кэша нет, получаем объекты из базы и кешируем их
        messages = MailMessage.objects.all()
        cache.set("messages", messages, 60 * 5)  # Кэшируем на 5 минут
        user = self.request.user
        if user.has_perm("mailapp.can_view_mail_message"):
            return MailMessage.objects.all()
        return MailMessage.objects.filter(owner=user)


class MailMessageCreateView(LoginRequiredMixin, CreateView):
    model = MailMessage
    template_name = "mailapp/mail_message_form.html"
    form_class = MailMessageForm
    success_url = reverse_lazy("mailapp:mail_message_list")

    def form_valid(self, form):
        message = form.save(commit=False)
        message.owner = self.request.user
        message.save()
        return redirect(reverse("mailapp:mail_message_list"))


class MailMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = MailMessage
    template_name = "mailapp/mail_message_form.html"
    form_class = MailMessageForm
    success_url = reverse_lazy("mailapp:mail_message_detail")

    def get_success_url(self):
        message = self.object
        return reverse_lazy("mailapp:mail_message_detail", kwargs={"pk": message.pk})


@method_decorator(cache_page(60 * 5), name="dispatch")  # Cache for 5 minutes
class MailMessageDetailView(LoginRequiredMixin, DetailView):
    model = MailMessage
    template_name = "mailapp/mail_message_detail.html"
    context_object_name = "message"


class MailMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MailMessage
    template_name = "mailapp/mail_message_confirm_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("mailapp:mail_message_list")


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    template_name = "mailapp/mailing_form.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailapp:mailing_list")

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.owner = self.request.user
        mailing.save()
        return redirect(reverse("mailapp:mailing_list"))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


@method_decorator(cache_page(60 * 5), name="dispatch")  # Cache for 5 minutes
class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailapp/mailing_detail.html"
    context_object_name = "mailing"

    def post(self, request, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=kwargs.get("pk"))
        if mailing.status == "Создана":
            MailingService.start_mailing(mailing)
            return redirect(reverse("mailapp:mailing_attempts"))
        elif mailing.status == "Запущена":
            if self.request.user.has_perm("mailapp.can_disabling_mailing") or self.request.user == mailing.owner:
                MailingService.stop_mailing(mailing)
                return redirect(reverse("mailapp:mailing_list"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipients"] = RecipientMail.objects.filter(mailing=self.object)
        return context


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    template_name = "mailapp/mailing_form.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailapp:mailing_detail")

    def get_success_url(self):
        mailing = self.object
        return reverse_lazy("mailapp:mailing_detail", kwargs={"pk": mailing.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailapp/mailing_list.html"
    context_object_name = "mailings"
    paginate_by = 10

    def get_queryset(self):
        cached_mailings = cache.get("mailings")
        if cached_mailings:
            return cached_mailings
        # Если кэша нет, получаем объекты из базы и кешируем их
        mailings = Mailing.objects.all()
        cache.set("mailings", mailings, 60 * 5)  # Кэшируем на 5 минут
        queryset = super().get_queryset()
        if self.request.user.has_perm("mailapp.can_view_mailing"):
            return Mailing.objects.all()
        return queryset.filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    context_object_name = "mailing"
    template_name = "mailapp/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailapp:mailing_list")


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailapp/mailing_attempt_list.html"
    context_object_name = "attempts"
    paginate_by = 10
    ordering = ["-date_mailing"]

    def get_queryset(self):
        cached_attempts = cache.get("attempts")
        if cached_attempts:
            return cached_attempts
        # Если кэша нет, получаем объекты из базы и кешируем их
        attempts = MailingAttempt.objects.all()
        cache.set("attempts", attempts, 60 * 5)  # Кэшируем на 5 минут
        queryset = super().get_queryset()
        return queryset.filter(mailing__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm("mailapp.can_view_mailing_attempt"):
            context["total_sent_messages"] = MailingAttempt.objects.filter(status="Успешно").count()
            context["total_failed_messages"] = MailingAttempt.objects.filter(status="Не успешно").count()
            return context
        else:
            context["total_sent_messages"] = MailingAttempt.objects.filter(
                status="Успешно", mailing__owner=self.request.user
            ).count()
            context["total_failed_messages"] = MailingAttempt.objects.filter(
                status="Не успешно", mailing__owner=self.request.user
            ).count()
            return context
