from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Post, Author, User, Category, CategorySubscribe
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail


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
        try:
            post.save()
        except ValueError as e:
            form.add_error(None, str(e))  # Добавляем ошибку в форму
            return self.form_invalid(form)
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

# Функция позволяющая подписаться на категорию
@login_required
def subscribe_to_category(request, pk):
    current_user = request.user
    category = get_object_or_404(Category, id=pk)  # Получаем категорию или 404

    # Проверяем, подписан ли пользователь на категорию
    if category.subscriber.filter(id=current_user.id).exists():
        message = 'Вы уже подписаны на рассылку постов этой категории.'
        return render(request, 'subscribe.html', {'category': category, 'message': message})

    # Если не подписан, добавляем подписчика
    category.subscriber.add(current_user)

    # Формируем сообщение
    message = f'Вы подписаны на рассылку постов категории {category.name}.'

    # Отправка почты
    send_mail(
        subject=f'Подписка на категорию: {category.name}',
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[current_user.email]
    )

    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    current_user = request.user
    category = Category.objects.get(id=pk)
    category.subscriber.remove(current_user)
    message = 'Вы успешно отписались от рассылки новостей категории'
    send_mail(
        subject=current_user.username,
        message=f'{message} {category}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[current_user.email]
    )
    return render(request, 'unsubscribe.html', {'category': category, 'message': message})
    
# Список категорий:
class CategoryList(ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'category'


class CategoryPost(DetailView):
    model = Category
    template_name = 'categories/post_category.html'
    context_object_name = 'postcategory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category=kwargs['object'])
        return context



