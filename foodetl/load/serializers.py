# food serailizer

from rest_framework import serializers
from .models import Food , FoodNutrient

class FoodNutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodNutrient
        fields = '__all__'

class FoodSerializer(serializers.ModelSerializer):

    food_nutrients = FoodNutrientSerializer(many=True)
    
    class Meta:
        model = Food
        fields = '__all__'
        
