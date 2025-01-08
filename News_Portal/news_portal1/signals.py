from django.db.models.signals import pre_save, post_save, m2m_changed
import datetime
from django.dispatch import receiver
from django.utils import timezone
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, CategorySubscribe, PostCategory


@receiver(pre_save, sender=Post)
def limit_posts_per_day(sender, instance, **kwargs):
    if instance.pk is None:  # Проверяем, что это новый пост
        today = timezone.now().date()
        post_count = Post.objects.filter(author=instance.author, time_add__date=today).count()
        if post_count >= 3:
            instance.error_message = "Вы не можете добавлять больше 3 постов в день."



# Отправка на почту подписчикам категории после публикации
def send_notifications(preview, pk, title, subscriber):
    html_content = render_to_string(
        'new_post_email.html',
        {
            'title': title,
            'text': preview,
            'link': f'http://127.0.0.1:8000/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscriber
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()



@receiver(m2m_changed, sender=PostCategory)
def weekly_notify(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':

        categories = instance.categories.all()
        subscribers_emails: list[str] = []
        for category in categories:
            subscribers_emails += category.subscriber.all()

        subscribers_emails = [s.email for s in subscribers_emails]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)