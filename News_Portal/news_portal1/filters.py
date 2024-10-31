from django.forms import DateInput, TextInput
from django import forms
from .models import Post, Category
from django_filters import FilterSet, CharFilter, DateFilter, ModelMultipleChoiceFilter  

class NewsFilter(FilterSet):
    author = CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Автор')
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Название', widget=TextInput(attrs={'style': 'width:100%;'}))
    search_date = DateFilter(field_name='time_add', lookup_expr='gte', label='Публикации от',
                             widget=DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    categories = ModelMultipleChoiceFilter(  
        field_name='categories',  
        queryset=Category.objects.all(),  
        label='Категории',  
        widget=forms.CheckboxSelectMultiple  # Можно использовать CheckboxSelectMultiple или SelectMultiple  
    )  
    class Meta:
        model = Post
        fields = ['author', 'title', 'search_date', 'categories']
