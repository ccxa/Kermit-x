from django.contrib import admin

from applications.common.models import PlatformAccount

@admin.register(PlatformAccount)
class PlatformAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_time', 'updated_time', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('name',)