from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import json
from .models import User, UserProfile, Notification
from django.utils import timezone
from datetime import timedelta


def index_view(request):
    """Home/Index page view - redirects based on authentication"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')


def signup_view(request):
    """Signup page view"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        return handle_signup(request)
    
    return render(request, 'signup.html')


@csrf_exempt
@require_http_methods(["POST"])
def handle_signup(request):
    """Handle signup form submission"""
    try:
        # Handle both JSON and FormData
        if 'application/json' in request.content_type:
            data = json.loads(request.body)
        else:
            # Handle FormData
            data = {}
            for key in request.POST:
                value = request.POST.get(key)
                # Handle checkbox values
                if key == 'terms' or key == 'newsletter':
                    data[key] = value == 'on' or value == 'true' or value == True
                else:
                    data[key] = value
        
        # Extract form data
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm-password', '')
        full_name = data.get('full-name', '').strip()
        cgpa = data.get('cgpa', '').strip()
        grades = data.get('grades', '').strip()
        
        # Validation
        errors = {}
        import re
        
        # Full Name Validation
        if not full_name:
            errors['full-name'] = 'Full name is required'
        elif len(full_name) > 50:
            errors['full-name'] = 'Full name must be 50 characters or less'
        elif not re.match(r'^[A-Za-z\s]+$', full_name):
            errors['full-name'] = 'Full name can only contain letters and spaces'
        
        # Email Validation
        if not email:
            errors['email'] = 'Email is required'
        elif len(email) > 254:
            errors['email'] = 'Email address is too long (max 254 characters)'
        elif not re.match(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$', email, re.IGNORECASE):
            errors['email'] = 'Please enter a valid email address'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists'
        
        # Password Validation
        if not password:
            errors['password'] = 'Password is required'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        elif len(password) > 128:
            errors['password'] = 'Password must be 128 characters or less'
        
        if password != confirm_password:
            errors['confirm-password'] = 'Passwords do not match'
        
        # CGPA Validation (optional, accepts any value)
        cgpa_value = None
        if cgpa:
            try:
                cgpa_value = float(cgpa) if cgpa else None
            except ValueError:
                # If not a valid number, store as None (optional field)
                cgpa_value = None
        
        # Grades Validation (numeric with optional %)
        if grades:
            if len(grades) > 10:
                errors['grades'] = 'Grades must be 10 characters or less'
            elif not re.match(r'^[0-9]+%?$', grades):
                errors['grades'] = 'Grades must be numeric with optional % sign (e.g., 85 or 85%)'
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=email,  # Use email as username
            email=email,
            password=password,
            full_name=full_name,
            program_level=data.get('program-level', ''),
            field_of_study=data.get('field-of-study', ''),
            cgpa=cgpa_value,
            grades=grades if grades else '',
            country=data.get('country', ''),
            preferred_country=data.get('preferred-country', ''),
            preferred_program_level=data.get('preferred-program-level', ''),
            budget_range=data.get('budget-range', ''),
            study_duration=data.get('study-duration', ''),
            newsletter_subscribed=data.get('newsletter', False) in (True, 'on', 'true', 'True'),
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        # Auto login after signup
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'redirect': '/dashboard/'
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Signup error: {error_trace}")  # Debug output
        return JsonResponse({
            'success': False,
            'errors': {'general': str(e)},
            'message': f'Error creating account: {str(e)}'
        }, status=500)


def login_view(request):
    """Login page view"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        return handle_login(request)
    
    return render(request, 'login.html')


@csrf_exempt
@require_http_methods(["POST"])
def handle_login(request):
    """Handle login form submission"""
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        remember_me = data.get('remember-me', False)
        
        errors = {}
        
        if not email:
            errors['email'] = 'Email is required'
        if not password:
            errors['password'] = 'Password is required'
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            # Handle remember me
            if not remember_me:
                request.session.set_expiry(0)  # Session expires when browser closes
            else:
                request.session.set_expiry(86400 * 30)  # 30 days
            
            return JsonResponse({
                'success': True,
                'redirect': '/dashboard/'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': {'email': 'Invalid email or password'}
            }, status=401)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': {'general': str(e)}
        }, status=500)


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')


@login_required
def dashboard_view(request):
    """Dashboard/Home page view with overview and recommended scholarships"""
    from scholarships.models import Scholarship, BookmarkedScholarship, ScholarshipApplication
    
    # Get user's profile info for matching
    user = request.user
    
    # Get recommended scholarships based on user profile
    recommended = Scholarship.objects.filter(is_active=True)
    
    # Filter by user's preferences
    if user.program_level:
        recommended = recommended.filter(program_level=user.program_level)
    if user.preferred_country:
        recommended = recommended.filter(study_country__icontains=user.preferred_country)
    if user.field_of_study:
        recommended = recommended.filter(field_of_study__icontains=user.field_of_study)
    
    # If no matches, show featured scholarships
    if not recommended.exists():
        recommended = Scholarship.objects.filter(is_active=True, is_featured=True)
    
    # Limit to 6 recommendations
    recommended = recommended[:6]
    
    # Get user stats
    total_bookmarks = BookmarkedScholarship.objects.filter(user=user).count()
    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
    
    return render(request, 'dashboard.html', {
        'recommended_scholarships': recommended,
        'total_bookmarks': total_bookmarks,
        'unread_notifications': unread_notifications,
        'user': request.user
    })


@login_required
def settings_view(request):
    """Settings page for user to edit profile, change password, etc."""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    context = {
        'user': user,
        'profile': profile,
    }
    
    return render(request, 'settings.html', context)


@login_required
def help_support_view(request):
    """Help and Support page"""
    return render(request, 'help_support.html')


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_profile(request):
    """Update user profile information"""
    try:
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Handle form data
        data = request.POST.dict() if hasattr(request.POST, 'dict') else dict(request.POST)
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]
        
        # Update User table fields separately
        if 'full_name' in data:
            user.full_name = data['full_name'][:50]  # Enforce 50 char limit
        if 'program_level' in data:
            user.program_level = data['program_level'] if data['program_level'] else None
        if 'field_of_study' in data:
            user.field_of_study = data['field_of_study'] if data['field_of_study'] else None
        if 'country' in data:
            user.country = data['country'] if data['country'] else None
        if 'cgpa' in data and data['cgpa']:
            try:
                user.cgpa = float(data['cgpa'])
            except (ValueError, TypeError):
                pass
        if 'grades' in data:
            user.grades = data['grades'] if data['grades'] else None
        if 'preferred_country' in data:
            user.preferred_country = data['preferred_country'] if data['preferred_country'] else None
        if 'preferred_program_level' in data:
            user.preferred_program_level = data['preferred_program_level'] if data['preferred_program_level'] else None
        if 'budget_range' in data:
            user.budget_range = data['budget_range'] if data['budget_range'] else None
        if 'study_duration' in data:
            user.study_duration = data['study_duration'] if data['study_duration'] else None
        if 'newsletter_subscribed' in data:
            user.newsletter_subscribed = data['newsletter_subscribed'] == 'on' or data['newsletter_subscribed'] == 'true' or data['newsletter_subscribed'] is True
        
        # Update UserProfile table fields separately
        if 'phone' in data:
            profile.phone = data['phone'] if data['phone'] else None
        if 'address' in data:
            profile.address = data['address'] if data['address'] else None
        if 'bio' in data:
            profile.bio = data['bio'] if data['bio'] else None
        
        # Save User and UserProfile tables separately
        user.save()
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully!'
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Profile update error: {error_trace}")
        return JsonResponse({
            'success': False,
            'message': f'Error updating profile: {str(e)}'
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def change_password(request):
    """Change user password"""
    try:
        user = request.user
        
        # Handle form data
        data = request.POST.dict() if hasattr(request.POST, 'dict') else dict(request.POST)
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]
        
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validation
        if not current_password or not new_password or not confirm_password:
            return JsonResponse({
                'success': False,
                'message': 'All password fields are required'
            }, status=400)
        
        if not user.check_password(current_password):
            return JsonResponse({
                'success': False,
                'message': 'Current password is incorrect'
            }, status=400)
        
        if len(new_password) < 8:
            return JsonResponse({
                'success': False,
                'message': 'New password must be at least 8 characters long'
            }, status=400)
        
        if new_password != confirm_password:
            return JsonResponse({
                'success': False,
                'message': 'New passwords do not match'
            }, status=400)
        
        # Update password
        user.set_password(new_password)
        user.save()
        
        # Re-login user with new password
        from django.contrib.auth import login
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Password changed successfully!'
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Password change error: {error_trace}")
        return JsonResponse({
            'success': False,
            'message': f'Error changing password: {str(e)}'
        }, status=500)


@login_required
def notifications_view(request):
    """View all notifications for the user"""
    # Get all notifications for the current user
    notifications_queryset = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications_queryset.filter(is_read=False).count()
    
    # Convert queryset to list to ensure it's evaluated
    notifications_list = list(notifications_queryset)
    
    context = {
        'notifications': notifications_list,
        'unread_count': unread_count,
        'user': request.user,  # Ensure user is in context
    }
    
    return render(request, 'notifications.html', context)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Notification marked as read'
        })
    except Notification.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Notification not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def delete_notification(request, notification_id):
    """Delete a single notification"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Notification deleted successfully'
        })
    except Notification.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Notification not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def delete_selected_notifications(request):
    """Delete selected notifications"""
    try:
        import json
        data = json.loads(request.body)
        notification_ids = data.get('notification_ids', [])
        
        if not notification_ids:
            return JsonResponse({
                'success': False,
                'message': 'No notifications selected'
            }, status=400)
        
        deleted_count = Notification.objects.filter(
            id__in=notification_ids,
            user=request.user
        ).delete()[0]
        
        return JsonResponse({
            'success': True,
            'message': f'{deleted_count} notification(s) deleted successfully',
            'deleted_count': deleted_count
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def delete_all_notifications(request):
    """Delete all notifications for the user"""
    try:
        deleted_count = Notification.objects.filter(user=request.user).delete()[0]
        
        return JsonResponse({
            'success': True,
            'message': f'All {deleted_count} notification(s) deleted successfully',
            'deleted_count': deleted_count
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    try:
        updated = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return JsonResponse({
            'success': True,
            'message': f'{updated} notifications marked as read'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
def get_unread_count(request):
    """Get unread notification count (API endpoint)"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({
        'unread_count': count
    })

