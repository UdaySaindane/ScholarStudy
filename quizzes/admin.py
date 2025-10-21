# from django.contrib import admin
# from .models import Quiz, Question, QuizAttempt

# class QuestionInline(admin.TabularInline):
#     model = Question
#     extra = 1
#     fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'points', 'order']

# @admin.register(Quiz)
# class QuizAdmin(admin.ModelAdmin):
#     list_display = ['title', 'course', 'passing_score', 'time_limit_minutes', 'is_active', 'created_at']
#     list_filter = ['is_active', 'course', 'created_at']
#     search_fields = ['title', 'course__title']
#     inlines = [QuestionInline]
    
#     fieldsets = (
#         ('Basic Information', {
#             'fields': ('course', 'title', 'description')
#         }),
#         ('Settings', {
#             'fields': ('passing_score', 'time_limit_minutes', 'max_attempts', 'is_active')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ['quiz', 'question_text_short', 'correct_answer', 'points', 'order']
#     list_filter = ['quiz', 'correct_answer']
#     search_fields = ['question_text', 'quiz__title']
#     ordering = ['quiz', 'order']
    
#     def question_text_short(self, obj):
#         return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
#     question_text_short.short_description = 'Question'

# @admin.register(QuizAttempt)
# class QuizAttemptAdmin(admin.ModelAdmin):
#     list_display = ['enrollment', 'quiz', 'score', 'percentage', 'passed', 'attempt_number', 'started_at']
#     list_filter = ['passed', 'quiz', 'started_at']
#     search_fields = ['enrollment__student__username', 'quiz__title']
#     readonly_fields = ['started_at', 'completed_at', 'time_taken']
    
#     fieldsets = (
#         ('Attempt Information', {
#             'fields': ('enrollment', 'quiz', 'attempt_number')
#         }),
#         ('Results', {
#             'fields': ('score', 'total_questions', 'percentage', 'passed')
#         }),
#         ('Answers', {
#             'fields': ('answers',),
#             'classes': ('collapse',)
#         }),
#         ('Timing', {
#             'fields': ('started_at', 'completed_at', 'time_taken'),
#             'classes': ('collapse',)
#         }),
#     )
from django.contrib import admin
from .models import Quiz, Question, QuizAttempt

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'points', 'order']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'passing_score', 'time_limit_minutes', 'is_active', 'created_at']
    list_filter = ['is_active', 'course', 'created_at']
    search_fields = ['title', 'course__title']
    inlines = [QuestionInline]

    # ✅ only editable fields go here
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'title', 'description')
        }),
        ('Settings', {
            'fields': ('passing_score', 'time_limit_minutes', 'max_attempts', 'is_active')
        }),
    )

    # ✅ created_at and updated_at are read-only
    readonly_fields = ['created_at', 'updated_at']

    # optional: show timestamps collapsed in admin detail view
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            fieldsets += (
                ('Timestamps', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                }),
            )
        return fieldsets


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_text_short', 'correct_answer', 'points', 'order']
    list_filter = ['quiz', 'correct_answer']
    search_fields = ['question_text', 'quiz__title']
    ordering = ['quiz', 'order']
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question'


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'quiz', 'score', 'percentage', 'passed', 'attempt_number', 'started_at']
    list_filter = ['passed', 'quiz', 'started_at']
    search_fields = ['enrollment__student__username', 'quiz__title']
    readonly_fields = ['started_at', 'completed_at', 'time_taken']
    
    fieldsets = (
        ('Attempt Information', {
            'fields': ('enrollment', 'quiz', 'attempt_number')
        }),
        ('Results', {
            'fields': ('score', 'total_questions', 'percentage', 'passed')
        }),
        ('Answers', {
            'fields': ('answers',),
            'classes': ('collapse',)
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at', 'time_taken'),
            'classes': ('collapse',)
        }),
    )
