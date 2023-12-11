from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['user']
    list_display = ['user', 'nickname', 'date_birth', 'location', Profile.about_you]
    list_editable = ['nickname', 'date_birth', 'location']

    readonly_fields = [
        'preview_photo',
    ]

    @staticmethod
    def preview_photo(obj):
        return mark_safe(f'<img src="{obj.photo.url}" style="max-height: 200px">')
