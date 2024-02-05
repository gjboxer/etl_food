from django.urls import path
from . import views

urlpatterns = [
    path('recipie/', views.RecipeView.as_view(), name='recipie-list')
]