from django.contrib import admin

# Register your models here.
from . import models
from django.utils.html import format_html


class ImageAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html(
            f'<img src="{obj.image.url}" style="max-width:200px; max-height:200px"/>'
        )

    list_display = [
        "name",
        "validated",
        "image_tag",
    ]


admin.site.register(models.CustomUser)
admin.site.register(models.Product, ImageAdmin)
admin.site.register(models.Rating)
admin.site.register(models.UserProductLink)
admin.site.register(models.Event)
admin.site.register(models.Todo)
