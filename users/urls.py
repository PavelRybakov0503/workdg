from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views import UserCreateView, email_verification, UserProfileUpdateView, UserProfileDetailView, UsersListView

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
    path(
        "reset_password/",
        PasswordResetView.as_view(
            template_name="users/registration/password_reset_form.html",
            email_template_name="users/registration/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        PasswordResetDoneView.as_view(template_name="users/registration/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<str:uidb64>/<str:token>",
        PasswordResetConfirmView.as_view(
            template_name="users/registration/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        PasswordResetCompleteView.as_view(template_name="users/registration/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("verify/<str:verification_token>/", email_verification, name="verify_email"),
    path("profile/<int:pk>/", UserProfileDetailView.as_view(), name="profile_detail"),
    path("profile/edit/<int:pk>/", UserProfileUpdateView.as_view(), name="edit_profile"),
    path("list/", UsersListView.as_view(), name="user_list"),
]
