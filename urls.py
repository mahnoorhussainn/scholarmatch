from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('help-support/', views.help_support_view, name='help_support'),
    path('api/signup/', views.handle_signup, name='api_signup'),
    path('api/login/', views.handle_login, name='api_login'),
    path('api/update-profile/', views.update_profile, name='update_profile'),
    path('api/change-password/', views.change_password, name='change_password'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('api/notifications/unread-count/', views.get_unread_count, name='get_unread_count'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('api/notifications/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    path('api/notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('api/notifications/delete-selected/', views.delete_selected_notifications, name='delete_selected_notifications'),
    path('api/notifications/delete-all/', views.delete_all_notifications, name='delete_all_notifications'),
]

