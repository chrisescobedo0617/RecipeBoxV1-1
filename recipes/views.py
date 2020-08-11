from django.shortcuts import render
from recipes.models import Author, Recipe

def homepage_view(request):
    return render(request, "homepage.html", {"recipes": Recipe.objects.all()})

def recipe_view(request, recipe_id):
    return render(request, "recipe.html", {"recipe": Recipe.objects.filter(id=recipe_id).first()})

def author_view(request, author_id):
    author_name = Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(author=author_name)
    return render(request, 'author.html', {"author": author_name, "recipes": recipes})