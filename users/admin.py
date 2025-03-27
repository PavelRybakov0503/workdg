from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'avatar', 'phone_number', 'area')
    search_fields = ('email', 'area')
    