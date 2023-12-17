from django.contrib import admin

from .models import GameProfile


@admin.register(GameProfile)
class GameProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['user']
    list_display = ['user', 'money', 'win', 'defeat']
    list_editable = ['money', 'win', 'defeat']
