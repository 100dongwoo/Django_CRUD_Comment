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
    phoneNumber = models.CharField(max_length=15,blank=True)

