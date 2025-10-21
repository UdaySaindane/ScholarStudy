from django.urls import path
from . import views

app_name = 'quizzes'
urlpatterns = [
    path('<int:enrollment_id>/<int:quiz_id>/start/', views.quiz_start, name='quiz_start'),
    path('<int:enrollment_id>/<int:quiz_id>/submit/', views.quiz_submit, name='quiz_submit'),
    path('result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('history/<int:enrollment_id>/', views.quiz_history, name='quiz_history'),

]