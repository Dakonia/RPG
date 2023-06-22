from django import forms
from .models import Post, Response
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class PostForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = [
            'tittle',
            'text',
            'category',
        ]



    def clean_tittle(self):
        tittle = self.cleaned_data["tittle"]
        if tittle[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return tittle

    def clean_text(self):
        text = self.cleaned_data["text"]
        if text[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return text


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40})
        }