# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db.models import Q
# from .models import Course, Category

# def course_list(request):
#     """List all published courses with filters"""
#     courses = Course.objects.filter(status='published')
#     categories = Category.objects.all()
    
#     # Search
#     query = request.GET.get('q')
#     if query:
#         courses = courses.filter(
#             Q(title__icontains=query) | 
#             Q(description__icontains=query)
#         )
    
#     # Filter by category
#     category_slug = request.GET.get('category')
#     if category_slug:
#         courses = courses.filter(category__slug=category_slug)
    
#     # Filter by price
#     price_filter = request.GET.get('price')
#     if price_filter == 'free':
#         courses = courses.filter(is_free=True)
#     elif price_filter == 'paid':
#         courses = courses.filter(is_free=False)
    
#     context = {
#         'courses': courses,
#         'categories': categories,
#         'query': query,
#     }
#     return render(request, 'courses/course_list.html', context)

# def course_detail(request, slug):
#     """Course detail page"""
#     course = get_object_or_404(Course, slug=slug, status='published')
#     lessons = course.lessons.all().order_by('order')
#     quizzes = course.quizzes.filter(is_active=True)
#     reviews = course.reviews.all().order_by('-created_at')[:5]
    
#     # Check if user is enrolled
#     is_enrolled = False
#     if request.user.is_authenticated:
#         is_enrolled = course.enrollments.filter(student=request.user).exists()
    
#     context = {
#         'course': course,
#         'lessons': lessons,
#         'quizzes': quizzes,
#         'reviews': reviews,
#         'is_enrolled': is_enrolled,
#     }
#     return render(request, 'courses/course_detail.html', context)

# @login_required
# def my_courses(request):
#     """Instructor's courses - Only for approved instructors"""
#     profile = request.user.profile
    
#     # Check if user is approved instructor
#     if profile.instructor_status != 'approved':
#         messages.error(request, 'You need to be an approved instructor to access this page.')
#         return redirect('accounts:profile')
    
#     # Check if in instructor mode
#     if profile.role != 'instructor':
#         messages.warning(request, 'Please switch to Instructor mode to manage courses.')
#         return redirect('accounts:profile')
    
#     courses = Course.objects.filter(instructor=request.user)
#     context = {'courses': courses}
#     return render(request, 'courses/my_courses.html', context)











from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Course, Category
from .forms import CourseForm, LessonForm, QuizForm, QuestionForm, QuizCSVUploadForm
from lessons.models import Lesson
from quizzes.models import Quiz, Question
import csv
import pandas as pd
from io import StringIO, BytesIO

def course_list(request):
    """List all published courses with filters"""
    courses = Course.objects.filter(status='published')
    categories = Category.objects.all()
    
    query = request.GET.get('q')
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    category_slug = request.GET.get('category')
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    
    price_filter = request.GET.get('price')
    if price_filter == 'free':
        courses = courses.filter(is_free=True)
    elif price_filter == 'paid':
        courses = courses.filter(is_free=False)
    
    context = {
        'courses': courses,
        'categories': categories,
        'query': query,
    }
    return render(request, 'courses/course_list.html', context)

def course_detail(request, slug):
    """Course detail page"""
    course = get_object_or_404(Course, slug=slug, status='published')
    lessons = course.lessons.all().order_by('order')
    quizzes = course.quizzes.filter(is_active=True)
    reviews = course.reviews.all().order_by('-created_at')[:5]
    
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = course.enrollments.filter(student=request.user).exists()
    
    context = {
        'course': course,
        'lessons': lessons,
        'quizzes': quizzes,
        'reviews': reviews,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def my_courses(request):
    """Instructor's courses"""
    profile = request.user.profile
    
    if profile.instructor_status != 'approved':
        messages.error(request, 'You need to be an approved instructor to access this page.')
        return redirect('accounts:profile')
    
    if profile.role != 'instructor':
        messages.warning(request, 'Please switch to Instructor mode to manage courses.')
        return redirect('accounts:profile')
    
    courses = Course.objects.filter(instructor=request.user)
    context = {'courses': courses}
    return render(request, 'courses/my_courses.html', context)

@login_required
def create_course(request):
    """Create a new course"""
    profile = request.user.profile
    
    if profile.instructor_status != 'approved' or profile.role != 'instructor':
        messages.error(request, 'Only approved instructors can create courses.')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, f'Course "{course.title}" created successfully!')
            return redirect('courses:manage_course', course_id=course.id)
    else:
        form = CourseForm(initial={'status': 'draft'})
    
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def edit_course(request, course_id):
    """Edit existing course"""
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('courses:manage_course', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})

@login_required
def manage_course(request, course_id):
    """Manage course - central dashboard for lessons, quizzes, etc."""
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    lessons = course.lessons.all().order_by('order')
    quizzes = course.quizzes.all()
    
    context = {
        'course': course,
        'lessons': lessons,
        'quizzes': quizzes,
    }
    return render(request, 'courses/manage_course.html', context)

@login_required
def add_lesson(request, course_id):
    """Add lesson to course"""
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, f'Lesson "{lesson.title}" added successfully!')
            return redirect('courses:manage_course', course_id=course.id)
    else:
        # Auto-set next order number
        last_lesson = course.lessons.order_by('-order').first()
        next_order = (last_lesson.order + 1) if last_lesson else 1
        form = LessonForm(initial={'order': next_order})
    
    return render(request, 'courses/add_lesson.html', {'form': form, 'course': course})

@login_required
def edit_lesson(request, lesson_id):
    """Edit lesson"""
    lesson = get_object_or_404(Lesson, id=lesson_id, course__instructor=request.user)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lesson updated successfully!')
            return redirect('courses:manage_course', course_id=lesson.course.id)
    else:
        form = LessonForm(instance=lesson)
    
    return render(request, 'courses/edit_lesson.html', {'form': form, 'lesson': lesson})

@login_required
def delete_lesson(request, lesson_id):
    """Delete lesson"""
    lesson = get_object_or_404(Lesson, id=lesson_id, course__instructor=request.user)
    course_id = lesson.course.id
    
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, 'Lesson deleted successfully!')
        return redirect('courses:manage_course', course_id=course_id)
    
    return render(request, 'courses/delete_lesson.html', {'lesson': lesson})

@login_required
def add_quiz(request, course_id):
    """Add quiz to course"""
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.success(request, f'Quiz "{quiz.title}" created! Now add questions.')
            return redirect('courses:manage_quiz', quiz_id=quiz.id)
    else:
        form = QuizForm(initial={'passing_score': 70, 'time_limit_minutes': 30, 'max_attempts': 3})
    
    return render(request, 'courses/add_quiz.html', {'form': form, 'course': course})

@login_required
def manage_quiz(request, quiz_id):
    """Manage quiz questions"""
    quiz = get_object_or_404(Quiz, id=quiz_id, course__instructor=request.user)
    questions = quiz.questions.all().order_by('order')
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'courses/manage_quiz.html', context)

@login_required
def add_question(request, quiz_id):
    """Add question to quiz manually"""
    quiz = get_object_or_404(Quiz, id=quiz_id, course__instructor=request.user)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'Question added successfully!')
            return redirect('courses:manage_quiz', quiz_id=quiz.id)
    else:
        # Auto-set next order
        last_question = quiz.questions.order_by('-order').first()
        next_order = (last_question.order + 1) if last_question else 1
        form = QuestionForm(initial={'order': next_order, 'points': 1})
    
    return render(request, 'courses/add_question.html', {'form': form, 'quiz': quiz})

@login_required
def upload_quiz_csv(request, quiz_id):
    """Upload quiz questions via CSV"""
    quiz = get_object_or_404(Quiz, id=quiz_id, course__instructor=request.user)
    
    if request.method == 'POST':
        form = QuizCSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            try:
                # Read CSV or Excel
                if csv_file.name.endswith('.csv'):
                    decoded_file = csv_file.read().decode('utf-8')
                    io_string = StringIO(decoded_file)
                    reader = csv.DictReader(io_string)
                    data = list(reader)
                else:  # Excel
                    df = pd.read_excel(csv_file)
                    data = df.to_dict('records')
                
                # Process questions
                created_count = 0
                for row in data:
                    Question.objects.create(
                        quiz=quiz,
                        question_text=row['question_text'],
                        option_a=row['option_a'],
                        option_b=row['option_b'],
                        option_c=row['option_c'],
                        option_d=row['option_d'],
                        correct_answer=row['correct_answer'].upper(),
                        points=int(row.get('points', 1)),
                        order=int(row.get('order', created_count + 1))
                    )
                    created_count += 1
                
                messages.success(request, f'{created_count} questions imported successfully!')
                return redirect('courses:manage_quiz', quiz_id=quiz.id)
                
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
    else:
        form = QuizCSVUploadForm()
    
    return render(request, 'courses/upload_quiz_csv.html', {'form': form, 'quiz': quiz})

@login_required
def delete_course(request, course_id):
    """Delete course"""
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('courses:my_courses')
    
    return render(request, 'courses/delete_course.html', {'course': course})