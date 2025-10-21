# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.utils import timezone
# from .models import Lesson
# from enrollments.models import Enrollment, LessonProgress

# @login_required
# def lesson_view(request, enrollment_id, lesson_id):
#     """View lesson content"""
#     enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
#     lesson = get_object_or_404(Lesson, id=lesson_id, course=enrollment.course)
    
#     # Get or create lesson progress
#     progress, created = LessonProgress.objects.get_or_create(
#         enrollment=enrollment,
#         lesson=lesson
#     )
    
#     context = {
#         'enrollment': enrollment,
#         'lesson': lesson,
#         'progress': progress,
#     }
#     return render(request, 'lessons/lesson_view.html', context)

# @login_required
# def mark_lesson_complete(request, enrollment_id, lesson_id):
#     """Mark lesson as complete"""
#     enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
#     lesson = get_object_or_404(Lesson, id=lesson_id, course=enrollment.course)
    
#     progress, created = LessonProgress.objects.get_or_create(
#         enrollment=enrollment,
#         lesson=lesson
#     )
    
#     if not progress.is_completed:
#         progress.is_completed = True
#         progress.completed_at = timezone.now()
#         progress.save()
        
#         # Update enrollment progress
#         enrollment.update_progress()
        
#         messages.success(request, f'Lesson "{lesson.title}" marked as complete!')
    
#     # Get next lesson
#     next_lesson = Lesson.objects.filter(
#         course=enrollment.course,
#         order__gt=lesson.order
#     ).order_by('order').first()
    
#     if next_lesson:
#         return redirect('lessons:lesson_view', enrollment_id=enrollment.id, lesson_id=next_lesson.id)
#     else:
#         messages.info(request, 'You have completed all lessons! Ready to take the quiz?')
#         return redirect('enrollments:course_player', enrollment_id=enrollment.id)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Lesson
from enrollments.models import Enrollment, LessonProgress

@login_required
def lesson_view(request, enrollment_id, lesson_id):
    """View lesson content"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=enrollment.course)
    
    # Get or create lesson progress
    progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )

    # Previous lesson
    previous_lesson = (
        enrollment.course.lessons
        .filter(order__lt=lesson.order)
        .order_by('-order')
        .first()
    )

    # Next lesson
    next_lesson = (
        enrollment.course.lessons
        .filter(order__gt=lesson.order)
        .order_by('order')
        .first()
    )

    context = {
        'enrollment': enrollment,
        'lesson': lesson,
        'progress': progress,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
    }
    return render(request, 'lessons/lesson_view.html', context)


@login_required
def mark_lesson_complete(request, enrollment_id, lesson_id):
    """Mark lesson as complete"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=enrollment.course)
    
    progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )
    
    if not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        
        # Update enrollment progress
        enrollment.update_progress()
        
        messages.success(request, f'Lesson "{lesson.title}" marked as complete!')

    # Get next lesson
    next_lesson = (
        enrollment.course.lessons
        .filter(order__gt=lesson.order)
        .order_by('order')
        .first()
    )
    
    if next_lesson:
        return redirect('lessons:lesson_view', enrollment_id=enrollment.id, lesson_id=next_lesson.id)
    else:
        messages.info(request, 'You have completed all lessons! Ready to take the quiz?')
        return redirect('enrollments:course_player', enrollment_id=enrollment.id)
