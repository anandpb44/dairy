from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Function to validate file size (limit to 5MB)
def validate_file_size(value):
    limit = 50 * 1024 * 1024  # 5 MB limit
    if value.size > limit:
        raise ValidationError("File size should not exceed 50 MB.")

# Function to validate image size (limit to 5MB)
def validate_image_size(value):
    limit = 50 * 1024 * 1024  # 5 MB limit
    if value.size > limit:
        raise ValidationError("Image size should not exceed 50 MB.")

# Function to validate image types (JPEG, PNG only)
def validate_image_type(value):
    if not value.name.lower().endswith(('jpg', 'jpeg', 'png')):
        raise ValidationError("Only JPEG and PNG images are allowed.")

class Document(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    file=models.FileField(upload_to='documents',validators=[validate_file_size])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
class Image(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    image=models.ImageField(upload_to='images',validators=[validate_image_size, validate_image_type])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    
class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title