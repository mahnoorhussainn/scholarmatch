from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50)
    
    # Academic Information
    program_level = models.CharField(
        max_length=50,
        choices=[
            ('bachelors', "Bachelor's Degree"),
            ('masters', "Master's Degree"),
            ('phd', 'PhD/Doctorate'),
            ('diploma', 'Diploma/Certificate'),
        ],
        blank=True,
        null=True
    )
    field_of_study = models.CharField(max_length=100, blank=True, null=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    grades = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Study Preferences
    preferred_country = models.CharField(max_length=100, blank=True, null=True)
    preferred_program_level = models.CharField(
        max_length=50,
        choices=[
            ('bachelors', "Bachelor's Degree"),
            ('masters', "Master's Degree"),
            ('phd', 'PhD/Doctorate'),
            ('diploma', 'Diploma/Certificate'),
            ('postgraduate-diploma', 'Postgraduate Diploma'),
            ('exchange-program', 'Exchange Program'),
            ('summer-school', 'Summer School'),
            ('research-fellowship', 'Research Fellowship'),
        ],
        blank=True,
        null=True
    )
    budget_range = models.CharField(max_length=50, blank=True, null=True)
    study_duration = models.CharField(max_length=50, blank=True, null=True)
    
    # Preferences
    newsletter_subscribed = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class UserProfile(models.Model):
    """Extended profile information for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - Profile"
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class Notification(models.Model):
    """Notification model for user notifications"""
    NOTIFICATION_TYPES = [
        ('deadline_approaching', 'Deadline Approaching'),
        ('deadline_soon', 'Deadline Soon'),
        ('deadline_today', 'Deadline Today'),
        ('new_scholarship', 'New Scholarship'),
        ('application_status', 'Application Status Update'),
        ('system', 'System Notification'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    # Optional link to related object
    scholarship = models.ForeignKey(
        'scholarships.Scholarship',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

