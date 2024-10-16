from django.db import models
from django.contrib.auth.models import User  

# Create your models here.

class Author(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    full_name = models.CharField(max_length=255)  
    age = models.IntegerField(blank=True, null=True)  
    email = models.EmailField(blank=True, null=True)
    rating = models.FloatField(default=0.0)
    
    def update_rating(self):
        post_ratings = sum(post.rating * 3 for post in self.post_set.all()) # суммарный рейтинг каждой статьи
        comment_ratings = sum(comment.rating for comment in self.user.comment_set.all()) # суммарный рейтинг всех комментариев автора
        article_comments_ratings = sum(comment.rating for post in self.post_set.all() for comment in post.comments.all()) # суммарный рейтинг всех комментариев к статьям автора
        self.rating = post_ratings + comment_ratings + article_comments_ratings  
        self.save()
    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
class Post(models.Model):
    ARTICLE = 'AR'  
    NEWS = 'NW'  
    TYPE_CHOICES = [(ARTICLE, 'Article'),(NEWS, 'News'),]
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  
    type_post = models.CharField(max_length=10, choices= TYPE_CHOICES)
    time_add = models.DateTimeField(auto_now_add=True)  
    categories = models.ManyToManyField(Category, through='PostCategory')  
    title = models.CharField(max_length = 255)
    content = models.TextField()
    rating = models.FloatField(default=0.0)
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating += 1
        self.save()
        
    def preview(self):
        return self.content[:124] + ('...' if len(self.content) > 124 else '')  
    
   
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time_add = models.DateTimeField(auto_now_add=True)  
    rating = models.FloatField(default=0.0) 
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating += 1
        self.save()