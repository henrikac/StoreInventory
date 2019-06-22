from collections import OrderedDict
import csv
from datetime import datetime
from typing import Dict, List


def read_csv(filename: str) -> List[OrderedDict]:
    """Reads data from a .csv file"""
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return [product for product in reader]



def clean_data(products: List[OrderedDict]) -> List[Dict]:
    """Cleans the provided data"""
    cleaned_data: List[Dict] = []

    for product in products:
        temp = dict(product)

        for key, value in product.items():
            if key == 'product_price':
                temp[key] = int(float(value[1:]) * 100)  # converts into cents
            elif key == 'product_quantity':
                temp[key] = int(value)
            elif key == 'date_updated':
                temp[key] = datetime.strptime(value, '%m/%d/%Y')

        cleaned_data.append(temp)

    return cleaned_data


if __name__ == '__main__':
    pass

