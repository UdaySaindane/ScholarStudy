# from django.contrib import admin
# from .models import Lesson

# @admin.register(Lesson)
# class LessonAdmin(admin.ModelAdmin):
#     list_display = ['title', 'course', 'content_type', 'order', 'is_preview', 'created_at']
#     list_filter = ['content_type', 'is_preview', 'course', 'created_at']
#     search_fields = ['title', 'course__title']
#     ordering = ['course', 'order']
    
#     fieldsets = (
#         ('Basic Information', {
#             'fields': ('course', 'title', 'content_type', 'order')
#         }),
#         ('Content', {
#             'fields': ('file_upload', 'text_content')
#         }),
#         ('Settings', {
#             'fields': ('duration_minutes', 'is_preview')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )

from django.contrib import admin
from .models import Lesson

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'content_type', 'order', 'is_preview', 'created_at']
    list_filter = ['content_type', 'is_preview', 'course', 'created_at']
    search_fields = ['title', 'course__title']
    ordering = ['course', 'order']

    # ✅ Only keep editable fields in fieldsets
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'title', 'content_type', 'order')
        }),
        ('Content', {
            'fields': ('file_upload', 'text_content')
        }),
        ('Settings', {
            'fields': ('duration_minutes', 'is_preview')
        }),
    )

    # ✅ Add timestamps as readonly fields so they display but aren’t editable
    readonly_fields = ['created_at', 'updated_at']
