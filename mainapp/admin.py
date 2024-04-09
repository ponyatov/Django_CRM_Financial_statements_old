from django.contrib import admin

from .models import Operations


class OperationsAdmin(admin.ModelAdmin):
    list_display = (
        'get_user_full_name',
        'reports',
        'counterparty',
        'value',
        'description',
        'image_cheque',
    )

    list_display_links = ('get_user_full_name', 'reports', 'counterparty', 'description', 'value', 'image_cheque')
    search_fields = ('user__first_name', 'user__last_name', 'reports', 'description', 'value')  # Обновляем для поиска
    list_filter = ('user__last_name', 'reports', 'description')  # Обновляем для фильтрации

    readonly_fields = ('reports', 'user')

    def get_user_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else ''

    get_user_full_name.short_description = 'Проектный менеджер'  # Задаем короткое описание поля


admin.site.register(Operations, OperationsAdmin)

admin.site.site_header = 'Intetix Администрирование отчётов'
admin.site.site_title = 'Администрирование отчётов'
