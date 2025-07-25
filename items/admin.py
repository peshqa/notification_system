from django.contrib import admin
from .models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner', 'created_at')
    list_filter = ('owner', 'created_at')
    search_fields = ('name', 'description')

    # Разрешить доступ только к своим записям
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    # Автоматически устанавливать владельца при создании
    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    # Разрешить доступ к модели для обычных пользователей
    def has_module_permission(self, request):
        return request.user.is_authenticated and request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.is_staff

    def has_change_permission(self, request, obj=None):
        if obj and obj.owner != request.user and not request.user.is_superuser:
            return False
        return request.user.is_authenticated and request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        if obj and obj.owner != request.user and not request.user.is_superuser:
            return False
        return request.user.is_authenticated and request.user.is_staff

admin.site.register(Item, ItemAdmin)