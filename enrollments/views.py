# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Enrollment
# from courses.models import Course

# @login_required
# def my_enrollments(request):
#     """Student's enrolled courses dashboard"""
#     enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
#     context = {
#         'enrollments': enrollments,
#     }
#     return render(request, 'enrollments/my_enrollments.html', context)

# @login_required
# def enroll_course(request, course_id):
#     """Enroll in a course"""
#     course = get_object_or_404(Course, id=course_id, status='published')
    
#     # Check if already enrolled
#     if Enrollment.objects.filter(student=request.user, course=course).exists():
#         messages.warning(request, 'You are already enrolled in this course.')
#         return redirect('courses:course_detail', slug=course.slug)
    
#     # Create enrollment
#     enrollment = Enrollment.objects.create(
#         student=request.user,
#         course=course,
#         payment_status='free' if course.is_free else 'pending',
#         amount_paid=0.00 if course.is_free else course.price
#     )
    
#     if course.is_free:
#         messages.success(request, f'Successfully enrolled in {course.title}!')
#         return redirect('enrollments:course_player', enrollment_id=enrollment.id)
#     else:
#         # Redirect to mock payment
#         return redirect('payments:checkout', course_id=course.id)

# @login_required
# def course_player(request, enrollment_id):
#     """Course learning interface"""
#     enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
#     lessons = enrollment.course.lessons.all().order_by('order')
#     quizzes = enrollment.course.quizzes.filter(is_active=True)
    
#     context = {
#         'enrollment': enrollment,
#         'course': enrollment.course,
#         'lessons': lessons,
#         'quizzes': quizzes,
#     }
#     return render(request, 'enrollments/course_player.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Enrollment
from courses.models import Course


# -----------------------------------------------------
# 1️⃣  Student Dashboard: My Enrollments
# -----------------------------------------------------
@login_required
def my_enrollments(request):
    """Student's enrolled courses dashboard"""
    enrollments = (
        Enrollment.objects.filter(student=request.user)
        .select_related('course')
        .prefetch_related('lesson_progress')
    )

    # Add progress data for each enrollment
    for enrollment in enrollments:
        total_lessons = enrollment.lesson_progress.count()
        completed_lessons = enrollment.lesson_progress.filter(is_completed=True).count()
        progress_percent = (
            int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0
        )

        # Attach values dynamically to the object
        enrollment.total_lessons = total_lessons
        enrollment.completed_lessons = completed_lessons
        enrollment.progress_percent = progress_percent

        # Optional: Quiz stats (if you want to show on dashboard)
        enrollment.passed_quizzes = enrollment.quiz_attempts.filter(passed=True).values('quiz').distinct().count()
        enrollment.latest_attempt = enrollment.quiz_attempts.first()

    context = {
        'enrollments': enrollments,
    }
    return render(request, 'enrollments/my_enrollments.html', context)


# -----------------------------------------------------
# 2️⃣  Enroll in a Course
# -----------------------------------------------------
@login_required
def enroll_course(request, course_id):
    """Enroll in a course"""
    course = get_object_or_404(Course, id=course_id, status='published')
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, 'You are already enrolled in this course.')
        return redirect('courses:course_detail', slug=course.slug)
    
    # Create new enrollment
    enrollment = Enrollment.objects.create(
        student=request.user,
        course=course,
        payment_status='free' if course.is_free else 'pending',
        amount_paid=0.00 if course.is_free else course.price
    )
    
    if course.is_free:
        messages.success(request, f'Successfully enrolled in {course.title}!')
        return redirect('enrollments:course_player', enrollment_id=enrollment.id)
    else:
        # Redirect to payment (for paid courses)
        return redirect('payments:checkout', course_id=course.id)


# -----------------------------------------------------
# 3️⃣  Course Player: Lesson + Quiz Dashboard
# -----------------------------------------------------
@login_required
def course_player(request, enrollment_id):
    """Course learning interface"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    course = enrollment.course
    lessons = course.lessons.all().order_by('order')
    quizzes = course.quizzes.filter(is_active=True)

    # Lessons progress
    lesson_data = []
    for lesson in lessons:
        completed = enrollment.lesson_progress.filter(lesson=lesson, is_completed=True).exists()
        lesson_data.append({
            'lesson': lesson,
            'completed': completed,
        })

    # Progress calculation
    total_lessons = len(lesson_data)
    completed_lessons = sum(1 for l in lesson_data if l['completed'])
    progress_percentage = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0

    # Safe quiz data
    quiz_data = []
    for quiz in quizzes:
        if not quiz.id:  # skip invalid ones
            continue
        best_attempt = enrollment.quiz_attempts.filter(quiz=quiz, passed=True).first()
        quiz_data.append({
            'quiz': quiz,
            'passed': bool(best_attempt),
        })

    context = {
        'enrollment': enrollment,
        'course': course,
        'lessons': lesson_data,
        'quizzes': quiz_data,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'enrollments/course_player.html', context)
