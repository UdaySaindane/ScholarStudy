from django.shortcuts import render
from courses.models import Course, Category

def home(request):
    """Homepage view with featured courses"""
    featured_courses = Course.objects.filter(status='published').order_by('-created_at')[:6]
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_courses': featured_courses,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page"""
    return render(request, 'core/about.html')