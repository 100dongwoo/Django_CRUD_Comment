from django.contrib.gis import admin
from service.models.comment import *


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id", "post", "user", "created_at", "comment",
    )
