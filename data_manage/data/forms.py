from django import forms
from .models import *


class DocumentForm(forms.ModelForm):
    class Meta:
        model=Document
        fields=['title','file']
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        allowed_extensions = ['pdf', 'doc', 'docx']
        if file:
            extension = file.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise ValidationError("Only PDF, DOC, and DOCX files are allowed.")
        return file


class ImageForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=['title','image']
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        allowed_extensions = ['jpg', 'jpeg', 'png']
        if image:
            extension = image.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise ValidationError("Only JPG, JPEG, and PNG images are allowed.")
        return image


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'content']