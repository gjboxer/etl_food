from rest_framework import serializers
from .models import Recipe
from load.models import Food
from load.serializers import FoodSerializer
class RecepieSerializer(serializers.ModelSerializer):
    foods=serializers.SerializerMethodField()
    class Meta:
        model = Recipe
        fields = '__all__'

    def get_foods(self, obj):
        food=Food.objects.filter(recipes=obj)
        return FoodSerializer(food,many=True).data