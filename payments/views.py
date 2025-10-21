from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment
from courses.models import Course
from enrollments.models import Enrollment

@login_required
def checkout(request, course_id):
    """Mock checkout page"""
    course = get_object_or_404(Course, id=course_id, status='published')
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, 'You are already enrolled in this course.')
        return redirect('courses:course_detail', slug=course.slug)
    
    if request.method == 'POST':
        # Create mock payment
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            status='completed'
        )
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=request.user,
            course=course,
            payment_status='completed',
            amount_paid=course.price
        )
        
        messages.success(request, f'Payment successful! You are now enrolled in {course.title}.')
        return redirect('payments:payment_success', payment_id=payment.id)
    
    context = {'course': course}
    return render(request, 'payments/checkout.html', context)

@login_required
def payment_success(request, payment_id):
    """Payment success page"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    enrollment = Enrollment.objects.get(student=request.user, course=payment.course)
    
    context = {
        'payment': payment,
        'enrollment': enrollment,
    }
    return render(request, 'payments/payment_success.html', context)