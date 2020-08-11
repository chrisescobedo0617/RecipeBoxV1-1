from django.db import models

class Author(models.Model):
    name = models.CharField()
    bio = models.TextField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    time_required = models.CharField()
    instructions = models.TextField()

    def __str__(self):
        return self.title
