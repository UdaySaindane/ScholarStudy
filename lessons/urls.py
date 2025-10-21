from django.urls import path
from . import views

app_name = 'lessons'
urlpatterns = [
    path('<int:enrollment_id>/<int:lesson_id>/', views.lesson_view, name='lesson_view'),
    path('<int:enrollment_id>/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark_complete'),
]