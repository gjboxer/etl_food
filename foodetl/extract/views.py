from django.shortcuts import render
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import csv
from transform.transform_utils import transform_data
from load.load_utils import load_transform_data
from django.urls import reverse
from django.http import HttpResponseRedirect
from load.models import Food
from recipie.views import RecipeView

class ExtractView(APIView):

    API_URL='https://api.nal.usda.gov/fdc/v1/foods/search?dataType=Foundation&api_key=ASWAAeVgTEvWNGDPKFBYZa7DpxluZ37vf6hFCazN&query='
    


    @classmethod
    def extract_data(cls,rows):
        food_names=[]
        extract_food_data=[]
        # populate the food names
        for food in Food.objects.all():
            food_names.append(food.name.lower())
            # iterate through the rows

        for row in csv.reader(rows, delimiter=','):
                if row and row[0].lower() not in food_names:
                    print("searching for", row[0].lower())
                    data_types = ['Foundation', 'Survey%20%28FNDDS%29', 'SR%20Legacy']

                    for data_type in data_types:
                       food_data = requests.get(cls.API_URL.replace('Foundation', data_type) + row[0]).json()

                       if food_data['foods']:
                           print('data found', row[0])
                           food_data['name'] = row[0]
                           extract_food_data.append(food_data)
                           break
                    else:
                       print('data does not exist', row[0])
                else:
                   print("data found in db", row[0])

        return extract_food_data

    def get(self, request, *args, **kwargs):
        # show the html page
        return render(request, 'uploadtemplate.html')
    

    def post(self, request, *args, **kwargs):
        # take the csv file from the request
        file = request.FILES['csv_file']
        if not file.name.endswith('.csv'):
            return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)
        # read the file
        data = file.read().decode('utf-8')


        ## data cleaning

        # split the data into rows
        rows = data.split('\n')
        # remove the header
        rows.pop(0)
        # check if any row is not empty and if it is empty remove it
        rows = [row for row in rows if row]
        # apply data cleaning by removing the approstrophe
        rows = [row.replace("'", "") for row in rows]
        # remove duplicates
        rows = list(set(rows))

        # extract the data
        extracted_data = self.extract_data(rows)
        # transform the data
        transformed_data = transform_data(extracted_data)
        # load the data
        status_load_data= load_transform_data(transformed_data)

        if status_load_data=="Successfully loaded data":
        # redirect to the load page
            food_object_list = Food.objects.all()
            food_name_list=[food.name for food in food_object_list]
            receipe_raw_data = RecipeView.scrape_receipe_data(food_name_list)
            print("receipe_raw_data",receipe_raw_data)
            

            reversed_url = reverse('load')
            return HttpResponseRedirect(reversed_url)
        else:
            return Response({'message': 'Data not loaded'}, status=status.HTTP_400_BAD_REQUEST)