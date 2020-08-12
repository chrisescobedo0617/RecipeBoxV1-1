from django import forms
from recipes.models import Author, Recipe

class AddAuthorForm(forms.Form):
    name = forms.CharField(max_length=40)
    bio = forms.CharField(widget=forms.Textarea)

class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)