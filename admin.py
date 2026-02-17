from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, Notification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'username', 'program_level', 'country', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_active', 'program_level', 'country', 'created_at')
    search_fields = ('email', 'username', 'full_name')
    ordering = ('-created_at',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Personal Information', {'fields': ('full_name',)}),
        ('Academic Information', {
            'fields': ('program_level', 'field_of_study', 'cgpa', 'grades', 'country')
        }),
        ('Study Preferences', {
            'fields': ('preferred_country', 'preferred_program_level', 'budget_range', 'study_duration')
        }),
        ('Preferences', {'fields': ('newsletter_subscribed',)}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__email', 'user__full_name', 'phone')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__email', 'title', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'read_at')

