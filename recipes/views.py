from django.shortcuts import render
from recipes.models import Author, Recipe

def homepage_view(request):
    return render(request, "homepage.html", {"recipes": ""})