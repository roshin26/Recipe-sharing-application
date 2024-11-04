from django import forms
from .models import Recipe
from django.conf import settings
from django_quill.fields import QuillField 

class RecipeForm(forms.ModelForm):
    """Form to create a recipe"""

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "ingredients",
            "instructions",
            "image",
            "image_alt",
            "meal_type",
            "cuisine_types",
            "calories",
        ]
        # ingredients = forms.CharField(
        #     widget=forms.Textarea(attrs={"rows": 4, "cols": 40})
        # )
        # instructions = forms.CharField(
        #     widget=forms.Textarea(attrs={"rows": 4, "cols": 40})
        # )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5, "cols": 40}),
        }

        labels = {
            "title": "Recipe Title",
            "description": "Description",
            "ingredients": "Recipe Ingredients",
            "instructions": "Recipe Instructions",
            "image": "Recipe Image",
            "image_alt": "Describe Image",
            "meal_type": "Meal Type",
            "cuisine_types": "Cuisine Type",
            "calories": "Calories",
        }
    
    ingredients = QuillField()
    instructions = QuillField()
