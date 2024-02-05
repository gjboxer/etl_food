from django.shortcuts import render
from rest_framework.views import APIView
from load.models import Food
import requests
from bs4 import BeautifulSoup

# Create your views here.
class RecipeView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'recipetemplate.html')
    
    @classmethod
    def scrape_receipe_data(cls, food_name_list):
        receipe_data = []

        for food_name in food_name_list:
            url='https://www.allrecipes.com/search?q=' + food_name
            # do web scraping of each food receipe with the food name
            page = requests.head(url)
            print(page.status_code)
            # handle 405 error
            if page.status_code == 405:
                page = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/100.0.4896.75 Safari/537.36'})
            # handle 404 error
            if page.status_code == 404:
                print('Page not found')
                continue
            # parse the html
            soup = BeautifulSoup(page.content, 'html.parser')
            print(soup.prettify())
            # find the receipe data
            receipe = soup.find_all('article', class_='fixed-recipe-card')
            

        return receipe_data