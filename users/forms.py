from django import forms
from django.contrib.auth.forms import UserCreationForm
from email_validator import EmailNotValidError, validate_email

from .models import User


class StyleFormMixin:
    """
        Миксин для добавления стиля полям формы. Цель - обеспечить единый вид всех форм.
        Каждое поле получает CSS-класс "form-control" и соответствующий тип.
        """

    def init(self, *args, **kwargs):
        """Инициализация и добавление стилей к элементам формы."""
        super().init(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.EmailField):
                # Стилизация поля для email
                field.widget.attrs.update({"class": "form-control", "type": "email"})
            elif isinstance(field, forms.ImageField):
                # Стилизация поля для загрузки изображений
                field.widget.attrs.update({"class": "form-control", "type": "file"})
            elif isinstance(field, forms.BooleanField):
                # Стилизация поля для флажков
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                # Общая стилизация для остальных полей
                field.widget.attrs.update({"class": "form-control"})


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации пользователя, наследующая от UserCreationForm.
    Добавляет возможность стилизации полей и валидации email и номера телефона.
    """

    class Meta:
        model = User
        fields = ("email", "avatar", "phone_number", "area", "password1", "password2")

    def clean_email(self):
        """
        Валидация email. Проверяет корректность введённого email-адреса.
        Поднимает forms.ValidationError, если email-адрес недействителен.
        """
        email = self.cleaned_data.get("email")
        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise forms.ValidationError(str(e))
        return email

    def clean_phone_number(self):
        """
        Валидация номера телефона. Убедитесь, что он содержит только цифры.
        """
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone_number


class UserEditForm(StyleFormMixin, forms.ModelForm):
    """
    Форма редактирования пользователя. Позволяет пользователям обновлять свою информацию.
    Предоставляет стилизацию и валидацию полей email и номера телефона.
    """

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "avatar", "phone_number", "area")
        exclude = ("password1", "password2")

    def clean_email(self):
        """
        Валидация email. Проверяет корректность введённого email-адреса.
        Поднимает forms.ValidationError, если email-адрес недействителен.
        """
        email = self.cleaned_data.get("email")
        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise forms.ValidationError(str(e))
        return email

    def clean_phone_number(self):
        """
        Валидация номера телефона. Убедитесь, что он содержит только цифры.
        """
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone_number


class UserManagerEditForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для редактирования данных пользователя администратором.
    Позволяет администратору изменять статус активности пользователя.
    """

    class Meta:
        model = User
        fields = ("is_active",)
