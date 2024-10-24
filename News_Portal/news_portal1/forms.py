from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class NewsForm(forms.ModelForm):
    content = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['title', 'content', 'author','categories',]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("description")
        title = cleaned_data.get("title")

        if title == content:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data