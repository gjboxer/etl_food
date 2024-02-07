# Food Data Extractor

The **Food Data Extractor** is a Django web application that extracts, transforms, and loads food data from a CSV file into a database. It uses the USDA FoodData Central API to retrieve detailed information about various food items based on their names.

## Features

- Upload CSV file containing food names
- Extract data for each food item from the USDA FoodData Central API
- Transform the extracted data
- Load transformed data into the database
- Integration with RecipeView to scrape recipe data for loaded food items

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone <repository_url>
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run migrations to set up the database:

    ```bash
    python manage.py migrate
    ```

4. Start the development server:

    ```bash
    python manage.py runserver
    ```

## Usage

1. Access the web application through your browser at `http://localhost:8000/extract`.
2. Upload a CSV file containing food names using the provided form.
3. The application will extract data for each food item, transform it, and load it into the database.
4. After successful loading, the application will redirect to the load page, where you can view the loaded food items.

## Contributing

Contributions are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
