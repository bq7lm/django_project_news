from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Post, Author, User
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

class NewsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        return context
    


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'
    
    
class SearchNews(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    success_url = '/news/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(user=self.request.user)  # Получаем экземпляр Author для текущего пользователя
        if self.request.path == '/articles/create/':
            post.type_post = 'AR'
        post.save()
        return super().form_valid(form)



class NewsUpdate(UpdateView, DetailView):
    form_class = NewsForm
    model = Post
    context_object_name = 'news_search'
    template_name = 'news_edit.html'
    success_url = '/news/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authors'] = self.request.user.groups.filter(name = 'authors').exists()
        return context



class NewsDelete(DeleteView, DetailView):
    model = Post
    context_object_name = 'news_search'
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    success_url = '/news/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authors'] = self.request.user.groups.filter(name = 'authors').exists()
        return context