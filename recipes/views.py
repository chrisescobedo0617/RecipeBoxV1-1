from django.shortcuts import render, HttpResponseRedirect, reverse
from recipes.models import Author, Recipe
from recipes.forms import AddAuthorForm, AddRecipeForm

def homepage_view(request):
    return render(request, "homepage.html", {"recipes": Recipe.objects.all()})

def recipe_view(request, recipe_id):
    return render(request, "recipe.html", {"recipe": Recipe.objects.filter(id=recipe_id).first()})

def author_view(request, author_id):
    author_name = Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(author=author_name)
    return render(request, 'author.html', {"author": author_name, "recipes": recipes})

def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data.get('name'),
                bio=data.get('bio')
            )
            return HttpResponseRedirect(reverse("homepage"))
    
    form = AddAuthorForm()
    return render(request, "generic_form.html", {"form": form})

def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {"form": form})