# from django.urls import path
# from . import views

# app_name = 'courses'

# urlpatterns = [
#     path('', views.course_list, name='course_list'),
#     path('my-courses/', views.my_courses, name='my_courses'),
#     path('<slug:slug>/', views.course_detail, name='course_detail'),
# ]







from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Public views
    path('', views.course_list, name='course_list'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    
    # Instructor views
    path('instructor/my-courses/', views.my_courses, name='my_courses'),
    path('instructor/create/', views.create_course, name='create_course'),
    path('instructor/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('instructor/<int:course_id>/manage/', views.manage_course, name='manage_course'),
    path('instructor/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    
    # Lesson management
    path('instructor/<int:course_id>/add-lesson/', views.add_lesson, name='add_lesson'),
    path('instructor/lesson/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('instructor/lesson/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
    
    # Quiz management
    path('instructor/<int:course_id>/add-quiz/', views.add_quiz, name='add_quiz'),
    path('instructor/quiz/<int:quiz_id>/manage/', views.manage_quiz, name='manage_quiz'),
    path('instructor/quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('instructor/quiz/<int:quiz_id>/upload-csv/', views.upload_quiz_csv, name='upload_quiz_csv'),
]