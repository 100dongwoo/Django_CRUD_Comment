# Generated by Django 3.1.2 on 2022-03-09 07:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_auto_20220306_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likeUsers',
            field=models.ManyToManyField(blank=True, related_name='like_post_users', to=settings.AUTH_USER_MODEL, verbose_name='좋아요 선택한 유저목록'),
        ),
    ]
