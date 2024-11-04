from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Recipe
from .forms import RecipeForm

# Create your views here.


class Recipes(ListView):
    """view all recipes"""

    template_name = "recipes/recipes.html"
    model = Recipe
    context_object_name = "recipes"


class RecipeDetail(DetailView):
    """view the recipe"""

    template_name = "recipes/recipe_detail.html"
    model = Recipe
    context_object_name = "recipe"


class AddRecipe(LoginRequiredMixin, CreateView):
    """Add recipe view"""

    template_name = "recipes/add_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddRecipe, self).form_valid(form)

class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
     """ Delete a recipe"""
     model = Recipe
     success_url = "/recipes/"

     def test_func(self):
         return self.request.user == self.get_object().user
     
class EditRecipe(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    """ Edit a recipe"""
    template_name = "recipes/edit_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def test_func(self):
         return self.request.user == self.get_object().user

