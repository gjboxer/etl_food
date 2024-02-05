from django.db import models
from load.models import Food
# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ingrediants = models.TextField()
    foods = models.ManyToManyField(Food, related_name='recipes')

    def __str__(self):
        return self.name