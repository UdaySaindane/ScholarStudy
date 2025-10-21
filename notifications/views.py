from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Notification
from accounts.models import Profile

@login_required
def notification_list(request):
    """List all notifications for admin"""
    # Only admins can access
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Only admins can view notifications.')
        return redirect('core:home')
    
    notifications = Notification.objects.filter(recipient=request.user)
    
    # Filter by status
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'pending':
        notifications = notifications.filter(
            notification_type='instructor_request',
            related_profile_id__in=Profile.objects.filter(instructor_status='pending').values_list('id', flat=True)
        )
    elif status_filter == 'approved':
        notifications = notifications.filter(
            notification_type='instructor_request',
            related_profile_id__in=Profile.objects.filter(instructor_status='approved').values_list('id', flat=True)
        )
    elif status_filter == 'rejected':
        notifications = notifications.filter(
            notification_type='instructor_request',
            related_profile_id__in=Profile.objects.filter(instructor_status='rejected').values_list('id', flat=True)
        )
    elif status_filter == 'unread':
        notifications = notifications.filter(is_read=False)
    
    # Search
    query = request.GET.get('q')
    if query:
        notifications = notifications.filter(
            Q(title__icontains=query) | 
            Q(message__icontains=query) |
            Q(related_user__username__icontains=query)
        )
    
    context = {
        'notifications': notifications,
        'status_filter': status_filter,
        'query': query,
    }
    return render(request, 'notifications/notification_list.html', context)

@login_required
def instructor_request_detail(request, profile_id):
    """View instructor request details and take action"""
    # Only admins can access
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('core:home')
    
    profile = get_object_or_404(Profile, id=profile_id)
    user = profile.user
    
    # Mark notification as read
    notification = Notification.objects.filter(
        recipient=request.user,
        related_profile_id=profile_id,
        notification_type='instructor_request'
    ).first()
    if notification and not notification.is_read:
        notification.mark_as_read()
    
    context = {
        'profile': profile,
        'user': user,
        'notification': notification,
    }
    return render(request, 'notifications/instructor_request_detail.html', context)

@login_required
def approve_instructor(request, profile_id):
    """Approve instructor request"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('core:home')
    
    if request.method == 'POST':
        profile = get_object_or_404(Profile, id=profile_id)
        
        # Approve instructor
        from django.utils import timezone
        profile.instructor_status = 'approved'
        profile.role = 'instructor'
        profile.instructor_approved_date = timezone.now()
        profile.save()
        
        messages.success(request, f'Successfully approved {profile.user.username} as an instructor!')
        return redirect('notifications:notification_list')
    
    return redirect('notifications:instructor_request_detail', profile_id=profile_id)

@login_required
def reject_instructor(request, profile_id):
    """Reject instructor request"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('core:home')
    
    if request.method == 'POST':
        profile = get_object_or_404(Profile, id=profile_id)
        
        # Reject instructor
        profile.instructor_status = 'rejected'
        profile.save()
        
        messages.warning(request, f'Rejected {profile.user.username}\'s instructor application.')
        return redirect('notifications:notification_list')
    
    return redirect('notifications:instructor_request_detail', profile_id=profile_id)

@login_required
def delete_notification(request, notification_id):
    """Delete a notification"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('core:home')
    
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.delete()
        messages.success(request, 'Notification deleted.')
    
    return redirect('notifications:notification_list')

@login_required
def mark_as_read(request, notification_id):
    """Mark notification as read"""
    if not request.user.is_superuser:
        return redirect('core:home')
    
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.mark_as_read()
    
    return redirect('notifications:notification_list')

@login_required
def mark_all_as_read(request):
    """Mark all notifications as read"""
    if not request.user.is_superuser:
        return redirect('core:home')
    
    if request.method == 'POST':
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
    
    return redirect('notifications:notification_list')




































# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.db.models import Q
# from .models import Notification
# from accounts.models import Profile

# @login_required
# def notification_list(request):
#     """List all notifications for admin"""
#     # Only admins can access
#     if not request.user.is_superuser:
#         messages.error(request, 'Access denied. Only admins can view notifications.')
#         return redirect('core:home')
    
#     notifications = Notification.objects.filter(recipient=request.user)
    
#     # Filter by status
#     status_filter = request.GET.get('status', 'all')
#     if status_filter == 'pending':
#         notifications = notifications.filter(
#             notification_type='instructor_request',
#             related_profile_id__in=Profile.objects.filter(instructor_status='pending').values_list('id', flat=True)
#         )
#     elif status_filter == 'approved':
#         notifications = notifications.filter(
#             notification_type='instructor_request',
#             related_profile_id__in=Profile.objects.filter(instructor_status='approved').values_list('id', flat=True)
#         )
#     elif status_filter == 'rejected':
#         notifications = notifications.filter(
#             notification_type='instructor_request',
#             related_profile_id__in=Profile.objects.filter(instructor_status='rejected').values_list('id', flat=True)
#         )
#     elif status_filter == 'unread':
#         notifications = notifications.filter(is_read=False)
    
#     # Search
#     query = request.GET.get('q')
#     if query:
#         notifications = notifications.filter(
#             Q(title__icontains=query) | 
#             Q(message__icontains=query) |
#             Q(related_user__username__icontains=query)
#         )
    
#     context = {
#         'notifications': notifications,
#         'status_filter': status_filter,
#         'query': query,
#     }
#     return render(request, 'notifications/notification_list.html', context)

# @login_required
# def instructor_request_detail(request, profile_id):
#     """View instructor request details and take action"""
#     # Only admins can access
#     if not request.user.is_superuser:
#         messages.error(request, 'Access denied.')
#         return redirect('core:home')
    
#     profile = get_object_or_404(Profile, id=profile_id)
#     user = profile.user
    
#     # Mark notification as read when viewing details
#     notification = Notification.objects.filter(
#         recipient=request.user,
#         related_profile_id=profile_id,
#         notification_type='instructor_request'
#     ).first()
    
#     if notification and not notification.is_read:
#         notification.mark_as_read()
    
#     context = {
#         'profile': profile,
#         'user': user,
#         'notification': notification,
#     }
#     return render(request, 'notifications/instructor_request_detail.html', context)

# @login_required
# def approve_instructor(request, profile_id):
#     """Approve instructor request"""
#     if not request.user.is_superuser:
#         messages.error(request, 'Access denied.')
#         return redirect('core:home')
    
#     if request.method == 'POST':
#         profile = get_object_or_404(Profile, id=profile_id)
        
#         # Approve instructor
#         from django.utils import timezone
#         profile.instructor_status = 'approved'
#         profile.role = 'instructor'
#         profile.instructor_approved_date = timezone.now()
#         profile.save()
        
#         # Mark related notification as read
#         notification = Notification.objects.filter(
#             recipient=request.user,
#             related_profile_id=profile_id,
#             notification_type='instructor_request'
#         ).first()
        
#         if notification and not notification.is_read:
#             notification.mark_as_read()
        
#         messages.success(request, f'Successfully approved {profile.user.username} as an instructor!')
#         return redirect('notifications:notification_list')
    
#     return redirect('notifications:instructor_request_detail', profile_id=profile_id)

# @login_required
# def reject_instructor(request, profile_id):
#     """Reject instructor request"""
#     if not request.user.is_superuser:
#         messages.error(request, 'Access denied.')
#         return redirect('core:home')
    
#     if request.method == 'POST':
#         profile = get_object_or_404(Profile, id=profile_id)
        
#         # Reject instructor
#         profile.instructor_status = 'rejected'
#         profile.save()
        
#         # Mark related notification as read
#         notification = Notification.objects.filter(
#             recipient=request.user,
#             related_profile_id=profile_id,
#             notification_type='instructor_request'
#         ).first()
        
#         if notification and not notification.is_read:
#             notification.mark_as_read()
        
#         messages.warning(request, f'Rejected {profile.user.username}\'s instructor application.')
#         return redirect('notifications:notification_list')
    
#     return redirect('notifications:instructor_request_detail', profile_id=profile_id)

# @login_required
# def delete_notification(request, notification_id):
#     """Delete a notification"""
#     if not request.user.is_superuser:
#         messages.error(request, 'Access denied.')
#         return redirect('core:home')
    
#     if request.method == 'POST':
#         notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
#         notification.delete()
#         messages.success(request, 'Notification deleted.')
    
#     return redirect('notifications:notification_list')

# @login_required
# def mark_as_read(request, notification_id):
#     """Mark notification as read"""
#     if not request.user.is_superuser:
#         return redirect('core:home')
    
#     notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
#     notification.mark_as_read()
    
#     return redirect('notifications:notification_list')

# @login_required
# def mark_all_as_read(request):
#     """Mark all notifications as read"""
#     if not request.user.is_superuser:
#         return redirect('core:home')
    
#     if request.method == 'POST':
#         from django.utils import timezone
#         Notification.objects.filter(
#             recipient=request.user, 
#             is_read=False
#         ).update(
#             is_read=True, 
#             read_at=timezone.now()
#         )
#         messages.success(request, 'All notifications marked as read.')
    
#     return redirect('notifications:notification_list')