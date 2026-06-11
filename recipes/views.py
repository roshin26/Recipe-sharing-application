from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView,UpdateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.html import escape
from .models import Recipe
from .forms import RecipeForm
from django.contrib import messages
from .auditor import audit_ingredients

class Recipes(ListView):
    """view all recipes"""

    template_name = "recipes/recipes.html"
    model = Recipe
    context_object_name = "recipes"

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q', '').strip()
        query = escape(query)
        if query:
            recipes = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(instructions__icontains=query) |
                Q(cuisine_types__icontains=query) |
                Q(meal_type__icontains=query)
            )
        else:
            recipes = self.model.objects.all()
        return recipes


class RecipeDetail(DetailView):
    """view the recipe detail here"""

    template_name = "recipes/recipe_detail.html"
    model = Recipe
    context_object_name = "recipe"


class AddRecipe(LoginRequiredMixin, CreateView):
    """Adding here the recipe view"""

    template_name = "recipes/add_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Extract plain text from QuillField ingredients
        raw_ingredients = form.instance.ingredients.plain
        # Run the AI Auto-Tagger
        tags = audit_ingredients(raw_ingredients)
        form.instance.dietary_tags = tags
        return super(AddRecipe, self).form_valid(form)

class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
     """ Deleteing the recipe here"""
     model = Recipe
     success_url = "/recipes/"

     def test_func(self):
         if not self.request.user.is_authenticated:
          return False
         return self.request.user == self.get_object().user
     
class EditRecipe(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    """ Edit a recipe"""
    template_name = "recipes/edit_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def test_func(self):
         if not self.request.user.is_authenticated:
          return False
         return self.request.user == self.get_object().user
    def form_valid(self, form):
        # Re-run the AI Auto-Tagger on edit
        raw_ingredients = form.instance.ingredients.plain
        tags = audit_ingredients(raw_ingredients)
        form.instance.dietary_tags = tags
        return super(EditRecipe, self).form_valid(form)

