from django import forms
from email_validator import EmailNotValidError, validate_email

from .models import Mailing, MailMessage, RecipientMail


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})


class RecipientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = RecipientMail
        fields = ["email", "full_name", "comment"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise forms.ValidationError(str(e))
        return email


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["message", "recipients", "frequency"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["recipients"].queryset = RecipientMail.objects.filter(owner=user)
            self.fields["message"].queryset = MailMessage.objects.filter(owner=user)

    def clean_recipients(self):
        recipients = self.cleaned_data.get("recipients")
        if not recipients:
            raise forms.ValidationError("Вы должны указать получателей.")
        return recipients


class MailMessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = ["subject", "body"]
