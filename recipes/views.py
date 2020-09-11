from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from recipes.models import Author, Recipe
from recipes.forms import AddAuthorForm, AddRecipeForm, LoginForm, RegisterForm


def homepage_view(request):
    return render(request, "homepage.html", {"recipes": Recipe.objects.all()})


def recipe_view(request, recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id).first()
    favorite_status = False
    if request.user.is_authenticated:
        author = Author.objects.filter(name=request.user.username).first()
        favorites_recipes = author.favorites.all()
        for favorite in favorites_recipes:
            if recipe_id == favorite.id:
                favorite_status = True
    return render(request, "recipe.html", {"recipe": recipe, 'favorite_status': favorite_status})


def author_view(request, author_id):
    author_name = Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(recipe_author=author_name)
    return render(request, 'author.html', {"author": author_name, "recipes": recipes})


def favorite_recipe_view(request, author_id):
    author = Author.objects.filter(id=author_id).first()
    favorites = author.favorites.all()
    return render(request, 'favorite.html', {'favorites': favorites, 'author': author})


@login_required
def add_author(request):
    if request.user.is_superuser:
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
    else:
        return render(request, "error.html")


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def recipe_edit_view(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.user.username == recipe.recipe_author.name or request.user.is_superuser:
        if request.method == 'POST':
            form = AddRecipeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                recipe.title = data['title']
                recipe.recipe_author = data['recipe_author']
                recipe.description = data['description']
                recipe.time_required = data['time_required']
                recipe.instructions = data['instructions']
                recipe.save()

            return HttpResponseRedirect(reverse('recipe_view', args=[recipe.id]))

        data = {
            'title': recipe.title,
            'author': recipe.recipe_author,
            'description': recipe.description,
            'time_required': recipe.time_required,
            'instructions': recipe.instructions
        }
        form = AddRecipeForm(initial=data)
        return render(request, "generic_form.html", {"form": form})
    else:
        return render(request, "error.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get("next", reverse("homepage")))

    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get(
                "username"), password=data.get("password"))
            login(request, new_user)
            return HttpResponseRedirect(reverse("homepage"))

    form = RegisterForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def add_favorite_view(request, recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id).first()
    author = Author.objects.get(name=request.user.username)

    author.favorites.add(recipe)
    author.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_favorite_view(request, recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id).first()
    author = Author.objects.get(name=request.user.username)

    author.favorites.remove(recipe)
    author.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))
