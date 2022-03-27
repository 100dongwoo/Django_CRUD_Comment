from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_CHOICE = [
    ('M', 'Man'),
    ('W', 'Woman'),
]


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    gender = models.CharField(
        choices=GENDER_CHOICE,
        default="M",
        max_length=16,
    )

    phoneNumber = models.CharField(max_length=15, blank=True)

    followUser = models.ManyToManyField(
        to='User',
        related_name='follow_users',
        verbose_name='좋아요 선택한 유저목록',
        blank=True,
    )
