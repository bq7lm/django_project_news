# Generated by Django 5.1.2 on 2024-10-16 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_portal1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='titme_add',
            new_name='time_add',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='titme_add',
            new_name='time_add',
        ),
    ]
