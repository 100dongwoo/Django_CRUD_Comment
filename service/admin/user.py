from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin

from service.models.user import *


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = [
        'id',"username","password"
    ]
