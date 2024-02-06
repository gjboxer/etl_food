from rest_framework.views import APIView
from .models import Food
from .serializers import FoodSerializer
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render

class LoadView(APIView):

    def get(self, request):
        # show the food data
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        if not serializer.data:
            return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)
        return render(request, 'loadtemplate.html', {'foods': serializer.data})