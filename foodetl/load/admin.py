from django.contrib import admin
from .models import Food, FoodNutrient
# Register your models here.
admin.site.register(Food)
admin.site.register(FoodNutrient)