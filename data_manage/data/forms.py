from django import forms
from .models import *
class DocumentForm(forms.ModelForm):
    class Meta:
        model=Document
        fields=['title','file']

class ImageForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=['title','image']

class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'content']