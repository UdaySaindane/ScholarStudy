# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import Profile

# class InstructorRequestForm(forms.ModelForm):
#     """Form for requesting to become an instructor"""
#     class Meta:
#         model = Profile
#         fields = ['instructor_bio']
#         widgets = {
#             'instructor_bio': forms.Textarea(attrs={
#                 'rows': 5,
#                 'placeholder': 'Tell us about your teaching experience, qualifications, and why you want to become an instructor...',
#                 'class': 'form-control'
#             })
#         }
#         labels = {
#             'instructor_bio': 'Why do you want to become an instructor?'
#         }
#         help_texts = {
#             'instructor_bio': 'Please provide details about your background, expertise, and teaching goals (minimum 100 characters).'
#         }
    
#     def clean_instructor_bio(self):
#         bio = self.cleaned_data.get('instructor_bio')
#         if len(bio) < 100:
#             raise forms.ValidationError('Please provide at least 100 characters describing your qualifications.')
#         return bio


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    """Custom registration form with email field"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        }),
        help_text='Required. We will use this to contact you.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile"""
    # User fields
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    
    class Meta:
        model = Profile
        fields = ['phone', 'date_of_birth', 'bio', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 234 567 8900'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'phone': 'Phone Number',
            'date_of_birth': 'Date of Birth',
            'bio': 'Bio',
            'avatar': 'Profile Picture'
        }
        help_texts = {
            'phone': 'Optional. Format: +1 234 567 8900',
            'date_of_birth': 'Optional',
            'bio': 'Optional. Tell others about yourself',
            'avatar': 'Optional. Upload a profile picture (JPG, PNG)'
        }
    
    def __init__(self, *args, **kwargs):
        # Extract user instance
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Pre-fill user fields if user exists
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

class InstructorRequestForm(forms.ModelForm):
    """Form for requesting to become an instructor"""
    class Meta:
        model = Profile
        fields = ['instructor_bio']
        widgets = {
            'instructor_bio': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Tell us about your teaching experience, qualifications, and why you want to become an instructor...',
                'class': 'form-control'
            })
        }
        labels = {
            'instructor_bio': 'Why do you want to become an instructor?'
        }
        help_texts = {
            'instructor_bio': 'Please provide details about your background, expertise, and teaching goals (minimum 100 characters).'
        }
    
    def clean_instructor_bio(self):
        bio = self.cleaned_data.get('instructor_bio')
        if len(bio) < 100:
            raise forms.ValidationError('Please provide at least 100 characters describing your qualifications.')
        return bio