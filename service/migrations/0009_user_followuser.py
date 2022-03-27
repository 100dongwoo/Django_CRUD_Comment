# Generated by Django 3.1.2 on 2022-03-27 11:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_post_hitcount'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='FollowUser',
            field=models.ManyToManyField(blank=True, related_name='follow_users', to=settings.AUTH_USER_MODEL, verbose_name='좋아요 선택한 유저목록'),
        ),
    ]
