from django import forms
from .models import Models, Photo


class ModelsForm(forms.ModelForm):

    class Meta :
        model = Models
        fields = ['title', 'text', 'image1', 'image2', 'image3', 'image4', 'image5', 'category']


class PhotoForm(forms.ModelForm):

    class Meta :
        model = Photo
        fields = ['title', 'text', 'image1', 'image2', 'image3', 'image4', 'image5', 'category']
