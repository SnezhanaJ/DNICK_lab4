# Generated by Django 4.2.1 on 2023-06-02 20:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_alter_blockeduser_user_blocked_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='blocked_users',
            field=models.ManyToManyField(blank=True, related_name='blocked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]