from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from recipes.models import Author, Recipe
from recipes.forms import AddAuthorForm, AddRecipeForm, LoginForm, RegisterForm

def homepage_view(request):
    return render(request, "homepage.html", {"recipes": Recipe.objects.all()})

def recipe_view(request, recipe_id):
    return render(request, "recipe.html", {"recipe": Recipe.objects.filter(id=recipe_id).first()})

def author_view(request, author_id):
    author_name = Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(author=author_name)
    return render(request, 'author.html', {"author": author_name, "recipes": recipes})

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

@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get("username"), password=data.get("password"))
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
            new_user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
            login(request, new_user)
            return HttpResponseRedirect(reverse("homepage"))
    
    form = RegisterForm()
    return render(request, "generic_form.html", {"form": form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))