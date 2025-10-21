from django import forms
from .models import Course, Category
from lessons.models import Lesson
from quizzes.models import Quiz, Question

class CourseForm(forms.ModelForm):
    """Form for creating/editing courses"""
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'thumbnail', 'price', 'is_free', 'prerequisites', 'level', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe what students will learn in this course...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'is_free': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'prerequisites': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What should students know before taking this course?'
            }),
            'level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make thumbnail not required for editing
        self.fields['thumbnail'].required = False

class LessonForm(forms.ModelForm):
    """Form for creating/editing lessons"""
    class Meta:
        model = Lesson
        fields = ['title', 'content_type', 'file_upload', 'text_content', 'order', 'duration_minutes', 'is_preview']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lesson title'
            }),
            'content_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'file_upload': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.ppt,.pptx'
            }),
            'text_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Enter lesson content here...'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lesson order (1, 2, 3...)'
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in minutes'
            }),
            'is_preview': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file_upload'].required = False
        self.fields['text_content'].required = False

class QuizForm(forms.ModelForm):
    """Form for creating/editing quizzes"""
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'passing_score', 'time_limit_minutes', 'max_attempts', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quiz title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Quiz description (optional)'
            }),
            'passing_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '70',
                'min': '0',
                'max': '100'
            }),
            'time_limit_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '30 (0 for no limit)',
                'min': '0'
            }),
            'max_attempts': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '3 (0 for unlimited)',
                'min': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

class QuestionForm(forms.ModelForm):
    """Form for manually adding quiz questions"""
    class Meta:
        model = Question
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'points', 'order']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your question here...'
            }),
            'option_a': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option A'
            }),
            'option_b': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option B'
            }),
            'option_c': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option C'
            }),
            'option_d': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option D'
            }),
            'correct_answer': forms.Select(attrs={
                'class': 'form-select'
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'value': '1'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Question order'
            }),
        }

class QuizCSVUploadForm(forms.Form):
    """Form for uploading quiz questions via CSV"""
    csv_file = forms.FileField(
        label='Upload CSV File',
        help_text='Upload a CSV file with questions. Format: question_text, option_a, option_b, option_c, option_d, correct_answer, points',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.xlsx'
        })
    )
    
    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']
        if not file.name.endswith(('.csv', '.xlsx')):
            raise forms.ValidationError('Only CSV and Excel files are allowed.')
        return file