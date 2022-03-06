from django.contrib.gis import admin
from  service.models.post import *

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title", "content", "user"
    )
