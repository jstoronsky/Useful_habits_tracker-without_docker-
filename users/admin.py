from django.contrib import admin
from users.models import User
# Register your models here.


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'tg_username', 'chat_id', 'last_login')
