
def transform_data(extracted_data):
    # transform the data
    transformed_data = []
    for food_data in extracted_data:
        # get the food details
        food = food_data['foods'][0]
        food_name=food_data['name']
        print('food_name', food_name)
        # get the food nutrients
        if 'foodNutrients' not in food:
            food['foodNutrients'] = []
        food_nutrients = food['foodNutrients']
        # get the food name
        food_description= food['description']

        food_id = food['fdcId']

        food_object = {
            'food_name': food_name,
            'food_id': food_id,
            'nutrients': [],
            'description': food_description
        }
        # iterate through the food nutrients
        for food_nutrient in food_nutrients:
            # get the nutrient name
            nutrient_name = food_nutrient['nutrientName']
            # get the nutrient unit
            nutrient_unit = food_nutrient['unitName']
            # get the nutrient value
            nutrient_value = food_nutrient['value']
            # create a dictionary of the transformed data
            food_object['nutrients'].append({
                'name': nutrient_name,
                'unit': nutrient_unit,
                'value': nutrient_value
            })
        # append the transformed data to the list
        transformed_data.append(food_object)

    return transformed_data
    