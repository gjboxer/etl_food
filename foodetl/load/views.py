from rest_framework.views import APIView
from .models import Food
from .serializers import FoodSerializer

from django.shortcuts import render

class LoadView(APIView):

    def get(self, request):
        # show the food data
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)

        return render(request, 'loadtemplate.html', {'foods': serializer.data})