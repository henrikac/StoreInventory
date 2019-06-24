from collections import OrderedDict
import csv
from datetime import datetime
import os
from typing import Dict, List

import product as prod


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


def prompt_for_id() -> int:
    """Prompts the user for a product id"""
    while True:
        try:
            prod_id = int(input('Enter a product id: '))

            if prod_id < 1:
                raise ValueError
        except ValueError:
            print('Invalid input: Please enter a positive number')
        else:
            return prod_id


def clear_screen() -> None:
    """Clears the console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def view_product() -> None:
    """Display a product to the user"""
    prod_id = prompt_for_id()
    product = prod.get_product(prod_id)
    #import pdb; pdb.set_trace()

    if product:
        print()
        for key, value in product.items():
            print(f'{key.replace("_", " ")}: {value}')
    else:
        print('\n** Sorry, couldn\'t find a product with that id **')

    input('\nPress enter to continue...')
    clear_screen()


def add_product() -> None:
    """Adds a product to the database"""
    pass


def create_backup() -> None:
    """Creates a backup"""
    pass


def quit() -> None:
    """Exits the program"""
    prod.close_db()
    raise SystemExit


def run_app() -> None:
    """Main function that runs the program"""
    data = read_csv('inventory.csv')
    cleaned_data = clean_data(data)
    prod.open_db()
    prod.add_products_to_db(cleaned_data)

    inv_opt = False

    while True:
        clear_screen()
        print('=' * 15)
        print('STORE INVENTORY')
        print('=' * 15, end='\n\n')

        for key, value in menu.items():
            print(f'{key}) {value.__doc__}')

        if inv_opt:
            print('\n** Invalid option **')

        choice = input('\n> ')

        if choice in menu:
            inv_opt = False
            menu[choice]()
        else:
            inv_opt = True


menu = OrderedDict([
    ('v', view_product),
    ('a', add_product),
    ('b', create_backup),
    ('q', quit)
])


if __name__ == '__main__':
    run_app()

