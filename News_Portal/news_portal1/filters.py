from django.forms import DateInput, TextInput
from .models import Post
from django_filters import FilterSet, CharFilter, DateFilter

class NewsFilter(FilterSet):
    author = CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Автор')
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Название', widget=TextInput(attrs={'style': 'width:100%;'}))
    search_date = DateFilter(field_name='time_add', lookup_expr='gte', label='Публикации от',
                             widget=DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))

    class Meta:
        model = Post
        fields = ['author', 'title', 'search_date']
