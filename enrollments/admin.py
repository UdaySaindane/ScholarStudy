from django.contrib import admin
from .models import Enrollment, LessonProgress

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'payment_status', 'progress_percentage', 'is_completed', 'enrolled_date']
    list_filter = ['payment_status', 'is_completed', 'enrolled_date']
    search_fields = ['student__username', 'course__title']
    readonly_fields = ['enrolled_date', 'completion_date', 'last_accessed']
    
    fieldsets = (
        ('Enrollment Information', {
            'fields': ('student', 'course')
        }),
        ('Payment', {
            'fields': ('payment_status', 'amount_paid')
        }),
        ('Progress', {
            'fields': ('progress_percentage', 'is_completed')
        }),
        ('Timestamps', {
            'fields': ('enrolled_date', 'completion_date', 'last_accessed'),
            'classes': ('collapse',)
        }),
    )

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'is_completed', 'completed_at']
    list_filter = ['is_completed', 'completed_at']
    search_fields = ['enrollment__student__username', 'lesson__title']
    readonly_fields = ['completed_at']