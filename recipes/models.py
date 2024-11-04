from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.html import format_html
from django_quill.fields import QuillField

# choice types
MEAL_TYPES = (("Breakfast", "breakfast"), ("Lunch", "lunch"), ("Dinner", "dinner"))

CUISINE_TYPES = (
    ("african", "African"),
    ("american", "American"),
    ("caribbean", "Caribbean"),
    ("asian", "Asian"),
    ("middle_eastern", "Middle Eastern"),
    ("chinese", "Chinese"),
    ("indian", "Indian"),
    ("pakistani", "Pakistani"),
    ("indonesian", "Indonesian"),
    ("european", "European"),
    ("oceanic", "Oceanic"),
)


class Recipe(models.Model):
    """
    This is a model to create recipes
    """

    user = models.ForeignKey(
        User, related_name="recipe_owner", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=300, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    # instructions = models.TextField(max_length=10000, null=False, blank=False)
    # ingredients = models.TextField(max_length=10000, null=False, blank=False)
    instructions = QuillField() 
    ingredients = QuillField()
    image = CloudinaryField("image", null=False, blank=False)
    image_alt = models.CharField(max_length=100, null=False, blank=False)
    meal_type = models.CharField(max_length=50, choices=MEAL_TYPES, default="breakfast")
    cuisine_types = models.CharField(
        max_length=50, choices=CUISINE_TYPES, default="indian"
    )
    calories = models.IntegerField()
    posted_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-posted_date"]

    def __str__(self):
        return str(self.title)

    def image_url(self):
        if self.image:
            return format_html(
                '<a href="{}" target="_blank">Recipe_image</a>', self.image.url
            )
        return "No Image"

    image_url.short_description = "Image URL"
