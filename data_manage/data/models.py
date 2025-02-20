from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Document(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    file=models.FileField(upload_to='documents')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
class Image(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    image=models.ImageField(upload_to='images')
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