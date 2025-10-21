from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from lessons.models import Lesson

class Enrollment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('free', 'Free'),
        ('completed', 'Completed'),
        ('pending', 'Pending'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    
    # Payment info (mock)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='free')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Progress
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=False)
    
    # Timestamps
    enrolled_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
    
    def update_progress(self):
        """Calculate and update progress percentage"""
        total_lessons = self.course.lessons.count()
        total_quizzes = self.course.quizzes.count()
        
        if total_lessons == 0 and total_quizzes == 0:
            return 0
        
        completed_lessons = self.lesson_progress.filter(is_completed=True).count()
        passed_quizzes = self.quiz_attempts.filter(passed=True).values('quiz').distinct().count()
        
        total_items = total_lessons + total_quizzes
        completed_items = completed_lessons + passed_quizzes
        
        self.progress_percentage = (completed_items / total_items * 100) if total_items > 0 else 0
        
        if self.progress_percentage >= 100:
            self.is_completed = True
            if not self.completion_date:
                from django.utils import timezone
                self.completion_date = timezone.now()
        
        self.save()
        return self.progress_percentage
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_date']

class LessonProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.enrollment.student.username} - {self.lesson.title}"
    
    class Meta:
        unique_together = ['enrollment', 'lesson']
        ordering = ['lesson__order']