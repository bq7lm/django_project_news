from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news_portal1.models import Author


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group, created = Group.objects.get_or_create(name='authors')

    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)  
        if not Author.objects.filter(user=user).exists():
            Author.objects.create(user=user)  

    return redirect('/')
