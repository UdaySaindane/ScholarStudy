# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib import messages
# from django.utils import timezone
# from .models import Profile
# from .forms import InstructorRequestForm

# def register(request):
#     """User registration view - Everyone starts as student"""
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Registration successful! Welcome to LearnHub.')
#             return redirect('core:home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'accounts/register.html', {'form': form})

# @login_required
# def profile(request):
#     """User profile view"""
#     user = request.user

#     # Student statistics
#     enrolled_courses_count = 0
#     completed_courses_count = 0
#     if hasattr(user, 'enrollments'):
#         enrolled_courses_count = user.enrollments.count()
#         completed_courses_count = user.enrollments.filter(is_completed=True).count()

#     # Instructor statistics
#     courses_created_count = 0
#     published_courses_count = 0
#     total_students = 0
#     if hasattr(user, 'courses_taught'):
#         courses_created_count = user.courses_taught.count()
#         published_courses_count = user.courses_taught.filter(status='published').count()
#         for course in user.courses_taught.all():
#             total_students += course.get_student_count()

#     context = {
#         'user': user,
#         'enrolled_courses_count': enrolled_courses_count,
#         'completed_courses_count': completed_courses_count,
#         'courses_created_count': courses_created_count,
#         'published_courses_count': published_courses_count,
#         'total_students': total_students,
#     }
#     return render(request, 'accounts/profile.html', context)

# @login_required
# def request_instructor(request):
#     """Student requests to become an instructor"""
#     profile = request.user.profile
    
#     # Check if already instructor or pending
#     if profile.role == 'instructor' and profile.instructor_status == 'approved':
#         messages.info(request, 'You are already an approved instructor.')
#         return redirect('accounts:profile')
    
#     if profile.instructor_status == 'pending':
#         messages.warning(request, 'Your instructor request is already pending approval.')
#         return redirect('accounts:profile')
    
#     if request.method == 'POST':
#         form = InstructorRequestForm(request.POST, instance=profile)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.instructor_status = 'pending'
#             profile.instructor_request_date = timezone.now()
#             profile.save()
#             messages.success(request, 'Your instructor request has been submitted! You will be notified once approved.')
#             return redirect('accounts:profile')
#     else:
#         form = InstructorRequestForm(instance=profile)
    
#     return render(request, 'accounts/request_instructor.html', {'form': form})

# @login_required
# def switch_mode(request):
#     """Toggle between instructor and student mode"""
#     profile = request.user.profile
    
#     # Only approved instructors can switch
#     if profile.instructor_status != 'approved':
#         messages.error(request, 'You are not an approved instructor.')
#         return redirect('accounts:profile')
    
#     # Toggle role
#     if profile.role == 'student':
#         profile.role = 'instructor'
#         profile.save()
#         messages.success(request, 'Switched to Instructor mode. You can now manage your courses.')
#         return redirect('courses:my_courses')
#     else:
#         profile.role = 'student'
#         profile.save()
#         messages.success(request, 'Switched to Student mode. You can now focus on learning.')
#         return redirect('enrollments:my_enrollments')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Profile
from .forms import InstructorRequestForm, CustomUserCreationForm, ProfileEditForm
from notifications.models import Notification
from django.contrib.auth.models import User



def register(request):
    """User registration view - Everyone starts as student"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to LearnHub.')
            return redirect('core:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """User profile view"""
    user = request.user

    # Student statistics
    enrolled_courses_count = 0
    completed_courses_count = 0
    if hasattr(user, 'enrollments'):
        enrolled_courses_count = user.enrollments.count()
        completed_courses_count = user.enrollments.filter(is_completed=True).count()

    # Instructor statistics
    courses_created_count = 0
    published_courses_count = 0
    total_students = 0
    if hasattr(user, 'courses_taught'):
        courses_created_count = user.courses_taught.count()
        published_courses_count = user.courses_taught.filter(status='published').count()
        for course in user.courses_taught.all():
            total_students += course.get_student_count()

    context = {
        'user': user,
        'enrolled_courses_count': enrolled_courses_count,
        'completed_courses_count': completed_courses_count,
        'courses_created_count': courses_created_count,
        'published_courses_count': published_courses_count,
        'total_students': total_students,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    """Edit user profile"""
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            # Save profile fields
            profile = form.save()
            
            # Update user fields
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.email = form.cleaned_data.get('email')
            user.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=profile, user=user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})

# @login_required
# def request_instructor(request):
#     """Student requests to become an instructor"""
#     profile = request.user.profile
    
#     # Check if already instructor or pending
#     if profile.role == 'instructor' and profile.instructor_status == 'approved':
#         messages.info(request, 'You are already an approved instructor.')
#         return redirect('accounts:profile')
    
#     if profile.instructor_status == 'pending':
#         messages.warning(request, 'Your instructor request is already pending approval.')
#         return redirect('accounts:profile')
    
#     if request.method == 'POST':
#         form = InstructorRequestForm(request.POST, instance=profile)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.instructor_status = 'pending'
#             profile.instructor_request_date = timezone.now()
#             profile.save()
#             messages.success(request, 'Your instructor request has been submitted! You will be notified once approved.')
#             return redirect('accounts:profile')
#     else:
#         form = InstructorRequestForm(instance=profile)
    
#     return render(request, 'accounts/request_instructor.html', {'form': form})

@login_required
def request_instructor(request):
    """Student requests to become an instructor"""
    profile = request.user.profile
    
    # Check if already instructor or pending
    if profile.role == 'instructor' and profile.instructor_status == 'approved':
        messages.info(request, 'You are already an approved instructor.')
        return redirect('accounts:profile')
    
    if profile.instructor_status == 'pending':
        messages.warning(request, 'Your instructor request is already pending approval.')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = InstructorRequestForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.instructor_status = 'pending'
            profile.instructor_request_date = timezone.now()
            profile.save()
            
            # CREATE NOTIFICATION FOR ALL ADMINS
            admins = User.objects.filter(is_superuser=True)
            for admin in admins:
                Notification.objects.create(
                    recipient=admin,
                    notification_type='instructor_request',
                    title='New Instructor Application',
                    message=f'{request.user.username} has applied to become an instructor.',
                    related_user=request.user,
                    related_profile_id=profile.id,
                    action_url=f'/notifications/instructor-request/{profile.id}/'
                )
            
            messages.success(request, 'Your instructor request has been submitted! You will be notified once approved.')
            return redirect('accounts:profile')
    else:
        form = InstructorRequestForm(instance=profile)
    
    return render(request, 'accounts/request_instructor.html', {'form': form})




@login_required
def switch_mode(request):
    """Toggle between instructor and student mode"""
    profile = request.user.profile
    
    # Only approved instructors can switch
    if profile.instructor_status != 'approved':
        messages.error(request, 'You are not an approved instructor.')
        return redirect('accounts:profile')
    
    # Toggle role
    if profile.role == 'student':
        profile.role = 'instructor'
        profile.save()
        messages.success(request, 'Switched to Instructor mode. You can now manage your courses.')
        return redirect('courses:my_courses')
    else:
        profile.role = 'student'
        profile.save()
        messages.success(request, 'Switched to Student mode. You can now focus on learning.')
        return redirect('enrollments:my_enrollments')