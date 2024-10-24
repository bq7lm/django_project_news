from django.urls import path
# Импортируем созданные нами представления
from .views import NewsList, NewsDetail, SearchNews, NewsCreate, NewsUpdate, NewsDelete

urlpatterns = [
   path('', NewsList.as_view(),name = 'news_list'),
   path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('search/', SearchNews.as_view(), name='news_search'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', NewsCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
]