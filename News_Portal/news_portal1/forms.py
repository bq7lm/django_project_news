from django import forms  
from django.core.exceptions import ValidationError  
from .models import Post


class NewsForm(forms.ModelForm):
    content = forms.CharField(
        min_length=20,
        widget=forms.Textarea(attrs={
            'style': 'width: 100%; min-height: 150px;'  # Установите минимальную высоту
        })
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'style': 'width: 100%; line-height: 1.5;'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories',]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")  # Исправлено с "description" на "content"
        title = cleaned_data.get("title")

        if title == content:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data
