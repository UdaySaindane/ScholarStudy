from django.urls import path
from . import views

app_name = 'enrollments'
urlpatterns = [
    path('my-learning/', views.my_enrollments, name='my_enrollments'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('player/<int:enrollment_id>/', views.course_player, name='course_player'),
]