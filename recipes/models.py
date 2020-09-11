from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=40)
    bio = models.TextField()
    favorites = models.ManyToManyField(
        'Recipe', symmetrical=False, blank=True
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=40)

    recipe_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    time_required = models.CharField(max_length=10)
    instructions = models.TextField()

    def __str__(self):
        return self.title
