from django.db import models

class FoodNutrient(models.Model):
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    unit_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.amount} {self.unit_name}"
    
class Food(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    fdc_id = models.IntegerField(unique=True)
    food_nutrients = models.ManyToManyField(FoodNutrient, related_name='foods')

    def __str__(self):
        return self.name

