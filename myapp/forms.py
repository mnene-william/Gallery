from django import forms
from .models import Photo

class PhotoForm(form.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'tags']