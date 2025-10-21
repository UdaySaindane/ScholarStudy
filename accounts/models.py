from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    )
    
    INSTRUCTOR_STATUS_CHOICES = (
        ('none', 'Not Applied'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='profiles/avatars/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Instructor verification fields
    instructor_status = models.CharField(max_length=20, choices=INSTRUCTOR_STATUS_CHOICES, default='none')
    instructor_request_date = models.DateTimeField(null=True, blank=True)
    instructor_approved_date = models.DateTimeField(null=True, blank=True)
    instructor_bio = models.TextField(blank=True, help_text="Why do you want to become an instructor?")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()







# from django.db import models

# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# class Profile(models.Model):
#     ROLE_CHOICES = (
#         ('student', 'Student'),
#         ('instructor', 'Instructor'),
#     )
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
#     bio = models.TextField(blank=True)
#     avatar = models.ImageField(upload_to='profiles/avatars/', blank=True, null=True)
#     phone = models.CharField(max_length=15, blank=True)
#     date_of_birth = models.DateField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.user.username} - {self.role}"
    
#     class Meta:
#         verbose_name = 'Profile'
#         verbose_name_plural = 'Profiles'

# # Auto-create profile when user is created
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()