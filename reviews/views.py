from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from courses.models import Course
from enrollments.models import Enrollment

@login_required
def add_review(request, course_id):
    """Add review for a course"""
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is enrolled
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, 'You must be enrolled to review this course.')
        return redirect('courses:course_detail', slug=course.slug)
    
    # Check if already reviewed
    if Review.objects.filter(course=course, student=request.user).exists():
        messages.warning(request, 'You have already reviewed this course.')
        return redirect('courses:course_detail', slug=course.slug)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.create(
            course=course,
            student=request.user,
            rating=rating,
            comment=comment
        )
        
        messages.success(request, 'Thank you for your review!')
        return redirect('courses:course_detail', slug=course.slug)
    
    context = {'course': course}
    return render(request, 'reviews/add_review.html', context)