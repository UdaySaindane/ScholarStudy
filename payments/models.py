from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Mock payment details (no real processing)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    payment_method = models.CharField(max_length=50, default='mock')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title} - ${self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            import uuid
            self.transaction_id = f"MOCK-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']