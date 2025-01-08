from django.urls import path
# Импортируем созданные нами представления
from .views import NewsList, NewsDetail, SearchNews, NewsCreate, NewsUpdate, NewsDelete, subscribe_to_category, CategoryPost, CategoryList, unsubscribe

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
   path('category_list/', CategoryList.as_view(), name='category_list'),
   path('category/<int:pk>/', CategoryPost.as_view(), name='category'),
   path('category/<int:pk>/subscribe', subscribe_to_category, name='subscribe_to_category'),
   path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]