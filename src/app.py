from collections import OrderedDict
import csv
from datetime import datetime
from typing import Dict, List

import product


def read_csv(filename: str) -> List[OrderedDict]:
    """Reads data from a .csv file"""
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return [product for product in reader]


def convert_data(product: Dict) -> Dict:
    """Converts data in a dict"""
    for key, value in product.items():
        if key == 'product_price':
            product[key] = int(float(value[1:]) * 100)  # converts into cents
        elif key == 'product_quantity':
            product[key] = int(value)
        elif key == 'date_updated':
            product[key] = datetime.strptime(value, '%m/%d/%Y')

    return product


def clean_data(products: List[OrderedDict]) -> List[Dict]:
    """Cleans the provided data"""
    cleaned_data: List[Dict] = []

    for product in products:
        cleaned_data.append(convert_data(product))

    return cleaned_data



if __name__ == '__main__':
    data = read_csv('inventory.csv')
    cleaned_data = clean_data(data)
    product.open_db()
    product.add_products_to_db(cleaned_data)
    product.close_db()

