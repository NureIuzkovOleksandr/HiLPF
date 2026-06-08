from django.contrib import admin
from .models import CustomUser, UserActivityLog

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('role', 'date_joined')

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp', 'ip_address')
    search_fields = ('user__username',)
    list_filter = ('activity_type', 'timestamp')
