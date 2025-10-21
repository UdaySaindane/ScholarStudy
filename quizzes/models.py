from django.db import models

# Create your models here.
from django.db import models
from courses.models import Course

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Settings
    passing_score = models.IntegerField(default=70, help_text="Percentage required to pass")
    time_limit_minutes = models.PositiveIntegerField(default=30, help_text="Time limit in minutes (0 for no limit)")
    max_attempts = models.PositiveIntegerField(default=3, help_text="Maximum number of attempts (0 for unlimited)")
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_question_count(self):
        return self.questions.count()
    
    def get_total_points(self):
        return sum([q.points for q in self.questions.all()])
    
    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        ordering = ['-created_at']

class Question(models.Model):
    ANSWER_CHOICES = (
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    )
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    
    # Options
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    
    # Correct answer
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    
    # Points
    points = models.PositiveIntegerField(default=1)
    
    # Order
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"
    
    class Meta:
        ordering = ['order', 'created_at']

class QuizAttempt(models.Model):
    from enrollments.models import Enrollment
    
    enrollment = models.ForeignKey('enrollments.Enrollment', on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    
    # Score
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Status
    passed = models.BooleanField(default=False)
    attempt_number = models.PositiveIntegerField(default=1)
    
    # Answers (JSON format)
    answers = models.JSONField(default=dict, help_text="Student's answers: {question_id: answer}")
    
    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_taken = models.DurationField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.enrollment.student.username} - {self.quiz.title} - Attempt {self.attempt_number}"
    
    class Meta:
        ordering = ['-started_at']