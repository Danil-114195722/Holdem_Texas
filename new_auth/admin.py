from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ['email']
    list_display = ['email', 'is_active', 'is_staff', 'date_added']
    list_editable = ['is_active']
