from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "meal_type",
        "calories",
        "instructions",
        "ingredients",
        "image_url",
    )
    readonly_fields = ("image_url",)
    list_filter = ("meal_type",)
