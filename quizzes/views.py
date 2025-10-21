from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Quiz, QuizAttempt
from enrollments.models import Enrollment

@login_required
def quiz_start(request, enrollment_id, quiz_id):
    """Start quiz"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    quiz = get_object_or_404(Quiz, id=quiz_id, course=enrollment.course, is_active=True)
    
    # Check max attempts
    attempt_count = QuizAttempt.objects.filter(enrollment=enrollment, quiz=quiz).count()
    if quiz.max_attempts > 0 and attempt_count >= quiz.max_attempts:
        messages.error(request, f'You have reached the maximum number of attempts ({quiz.max_attempts}) for this quiz.')
        return redirect('enrollments:course_player', enrollment_id=enrollment.id)
    
    questions = quiz.questions.all().order_by('order')
    
    context = {
        'enrollment': enrollment,
        'quiz': quiz,
        'questions': questions,
        'attempt_number': attempt_count + 1,
    }
    return render(request, 'quizzes/quiz_take.html', context)

@login_required
def quiz_submit(request, enrollment_id, quiz_id):
    """Submit quiz and calculate score"""
    if request.method != 'POST':
        return redirect('quizzes:quiz_start', enrollment_id=enrollment_id, quiz_id=quiz_id)
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    quiz = get_object_or_404(Quiz, id=quiz_id, course=enrollment.course)
    
    questions = quiz.questions.all()
    total_questions = questions.count()
    correct_count = 0
    answers = {}
    
    # Calculate score
    for question in questions:
        student_answer = request.POST.get(f'question_{question.id}')
        answers[str(question.id)] = student_answer
        
        if student_answer == question.correct_answer:
            correct_count += 1
    
    percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    passed = percentage >= quiz.passing_score
    
    # Get attempt number
    attempt_count = QuizAttempt.objects.filter(enrollment=enrollment, quiz=quiz).count()
    
    # Create quiz attempt
    attempt = QuizAttempt.objects.create(
        enrollment=enrollment,
        quiz=quiz,
        score=correct_count,
        total_questions=total_questions,
        percentage=percentage,
        passed=passed,
        attempt_number=attempt_count + 1,
        answers=answers,
        completed_at=timezone.now()
    )
    
    # Update enrollment progress
    enrollment.update_progress()
    
    return redirect('quizzes:quiz_result', attempt_id=attempt.id)

@login_required
def quiz_result(request, attempt_id):
    """Show quiz results"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, enrollment__student=request.user)
    questions = attempt.quiz.questions.all().order_by('order')
    
    # Prepare results with correct/wrong info
    results = []
    for question in questions:
        student_answer = attempt.answers.get(str(question.id))
        is_correct = student_answer == question.correct_answer
        results.append({
            'question': question,
            'student_answer': student_answer,
            'is_correct': is_correct,
        })
    
    context = {
        'attempt': attempt,
        'results': results,
        'can_retake': attempt.quiz.max_attempts == 0 or attempt.attempt_number < attempt.quiz.max_attempts,
    }
    return render(request, 'quizzes/quiz_result.html', context)

@login_required
def quiz_history(request, enrollment_id):
    """View all quiz attempts for a course"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    attempts = QuizAttempt.objects.filter(enrollment=enrollment).order_by('-started_at')
    
    context = {
        'enrollment': enrollment,
        'attempts': attempts, 
    }
    return render(request, 'quizzes/quiz_history.html', context)