from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('instructor-request/<int:profile_id>/', views.instructor_request_detail, name='instructor_request_detail'),
    path('approve/<int:profile_id>/', views.approve_instructor, name='approve_instructor'),
    path('reject/<int:profile_id>/', views.reject_instructor, name='reject_instructor'),
    path('delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('mark-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
]