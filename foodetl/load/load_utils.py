from .models import Food, FoodNutrient
# Create your views here.


def load_transform_data(transform_data):
    # load the data
    for food in transform_data:
        food_name = food.pop('food_name')
        food_id = food.pop('food_id')
        food_description = food.pop('description')
        food_nutrients = food.pop('nutrients')
        # create the food object
        if Food.objects.filter(fdc_id=food_id).exists():
            print('food with id already exists')
            # then update the food name
            food_object = Food.objects.filter(name=food_name)
            food_object.name = food_name                
            continue

        elif Food.objects.filter(name=food_name).exists():
            print('food with name already exists')
            continue

        food_object = Food.objects.create(
            name=food_name,
            description=food_description,
            fdc_id=food_id
        )
        # create the food nutrients
        for food_nutrient in food_nutrients:
            nutrient_name = food_nutrient['name']
            nutrient_unit = food_nutrient['unit']
            nutrient_value = food_nutrient['value']
            food_nutrient_object = FoodNutrient.objects.create(
                name=nutrient_name,
                amount=nutrient_value,
                unit_name=nutrient_unit
            )
            food_nutrient_object.save()
            food_object.food_nutrients.add(food_nutrient_object)
        food_object.save()
    return "Successfully loaded data"
