from django.shortcuts import render
from rest_framework.views import APIView
from load.models import Food
import requests
from bs4 import BeautifulSoup
from recipie.models import Recipe
from recipie.serializers import RecepieSerializer
from rest_framework.response import Response
from rest_framework import status
from recipie.models import Food
from recipie.models import Recipe

# Create your views here.
class RecipeView(APIView):

    def get(self, request, *args, **kwargs):
        recipe_data=Recipe.objects.all()
        serializer = RecepieSerializer(recipe_data, many=True)
        recipe_data = serializer.data
        if not recipe_data:
            return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'recipe_data': recipe_data}, status=status.HTTP_200_OK)

    @classmethod
    def scrape_receipe_data(cls, food_name_list):
        recipe_data = []
        try:
            for food_name in food_name_list:
                url = 'https://www.allrecipes.com/search?q=' + food_name
                page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/100.0.4896.75 Safari/537.36'})

                if page.status_code == 404:
                    print(f'Page not found for {food_name}')
                    continue

                # Parse the HTML
                soup = BeautifulSoup(page.content, 'html.parser')
                # print(soup.prettify())
                print(f'Parsing HTML for {food_name}')
                recipe_data.append({'food_name': food_name, 'recipesurl': []})

                # Find the recipe data

                recipes = soup.find_all('a',class_='comp mntl-card-list-items mntl-document-card mntl-card card card--no-image')
                # get href of the recipe of first 3 recipes

                for recipe in recipes[:1]:
                    recipe_url = recipe['href']
                    recipe_data[-1]['recipesurl'].append(recipe_url)

                for data in recipe_data:
                    # scrape receipes from the urls
                    print(f'Parsing HTML for {data["food_name"]}')
                    for i, url in enumerate(data['recipesurl']):
                        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/100.0.4896.75 Safari/537.36'})
                        soup = BeautifulSoup(page.content, 'html.parser')
                        # get the recipe name
                        recipe_name = soup.find('h1',class_='comp type--lion article-heading mntl-text-block').text
                        print(recipe_name)
                        # # get the recipe description
                        recipe_description = soup.find('p', class_='comp type--dog article-subheading').text
                        # print(recipe_description)
                        # # get the recipe ingredients
                        ingredients = soup.find_all('span', {'data-ingredient-name': 'true'})
                        ingredients_list=[ingredient.text for ingredient in ingredients]
                        # print(ingredients_list)
                        directions = soup.find_all('p', class_="comp mntl-sc-block mntl-sc-block-html")
                        print(directions)
                        # extrtact text from the directions
                        directions_list=[direction.text for direction in directions]
                        # remove '\n' from each direction
                        directions_list = [direction.replace('\n', '') for direction in directions_list]
                        print(directions_list)
                        # Assuming directions_list contains your list of directions

                        recipe_data[i]['recipe'] = {'name': recipe_name, 'description': recipe_description, 'ingredients': ingredients_list, 'directions': directions_list}
                        if Recipe.objects.filter(name=recipe_name).exists():
                            print('recipe with name already exists')
                            continue

                        recipe = Recipe.objects.create(
                                name=recipe_name,
                                description=recipe_description,
                                ingrediants=ingredients_list,
                                directions=directions_list
                                )
                        food = Food.objects.get(name=data['food_name'])
                        recipe.foods.add(food)
                        recipe.save()

            return recipe_data
        except Exception as e:
            print(e)
            return recipe_data