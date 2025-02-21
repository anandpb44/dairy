from django.contrib import admin
from .models import Document, Image, DiaryEntry
# Register your models here.
admin.site.register(Document)
admin.site.register(Image)
admin.site.register(DiaryEntry)