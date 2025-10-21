from django.contrib import admin
from django.utils import timezone
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'instructor_status', 'phone', 'created_at']
    list_filter = ['role', 'instructor_status', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'instructor_request_date', 'instructor_approved_date']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Profile Details', {
            'fields': ('bio', 'avatar', 'phone', 'date_of_birth')
        }),
        ('Instructor Verification', {
            'fields': ('instructor_status', 'instructor_bio', 'instructor_request_date', 'instructor_approved_date'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_instructor', 'reject_instructor']
    
    def approve_instructor(self, request, queryset):
        """Approve instructor requests"""
        updated = 0
        for profile in queryset.filter(instructor_status='pending'):
            profile.instructor_status = 'approved'
            profile.role = 'instructor'
            profile.instructor_approved_date = timezone.now()
            profile.save()
            updated += 1
        self.message_user(request, f'{updated} instructor request(s) approved.')
    approve_instructor.short_description = "Approve selected instructor requests"
    
    def reject_instructor(self, request, queryset):
        """Reject instructor requests"""
        updated = queryset.filter(instructor_status='pending').update(instructor_status='rejected')
        self.message_user(request, f'{updated} instructor request(s) rejected.')
    reject_instructor.short_description = "Reject selected instructor requests"







# from django.contrib import admin
# from .models import Profile

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'role', 'phone', 'created_at']
#     list_filter = ['role', 'created_at']
#     search_fields = ['user__username', 'user__email', 'phone']
#     readonly_fields = ['created_at', 'updated_at']
    
#     fieldsets = (
#         ('User Information', {
#             'fields': ('user', 'role')
#         }),
#         ('Profile Details', {
#             'fields': ('bio', 'avatar', 'phone', 'date_of_birth')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
