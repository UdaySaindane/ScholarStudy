from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    comment = models.TextField()
    
    # Helpful votes (optional feature)
    helpful_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.rating}⭐"
    
    class Meta:
        unique_together = ['course', 'student']
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'