from django.db import models

# Create your models here.
from django.db import models
from courses.models import Course

class Lesson(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('pdf', 'PDF Document'),
        ('ppt', 'PowerPoint'),
        ('text', 'Text Content'),
    )
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    
    # File uploads
    file_upload = models.FileField(upload_to='lessons/files/', blank=True, null=True,
                                   help_text="Upload PDF or PPT file")
    
    # Text content
    text_content = models.TextField(blank=True, help_text="For text-based lessons")
    
    # Ordering
    order = models.PositiveIntegerField(default=0, help_text="Lesson sequence number")
    
    # Duration (optional, in minutes)
    duration_minutes = models.PositiveIntegerField(default=0, blank=True)
    
    # Preview (allow non-enrolled students to see)
    is_preview = models.BooleanField(default=False, help_text="Allow preview without enrollment")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_file_extension(self):
        if self.file_upload:
            return self.file_upload.name.split('.')[-1].lower()
        return None
    
    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['course', 'order']