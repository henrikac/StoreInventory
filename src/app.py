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


def prompt_for_product_name() -> str:
    """Prompts the user for a product name"""
    while True:
        prod_name = input('Enter product name: ')

        if len(prod_name.strip()) < 1:
            print('Please enter the product name')
        else:
            return prod_name


def prompt_for_int(str_value: str) -> int:
    """Prompts the user for an integer"""
    while True:
        try:
            result = int(input(str_value))

            if result < 0:
                raise ValueError
        except ValueError:
            print('Invalid input: Please enter a number greater than or equal to 0')
        else:
            return result


def clear_screen() -> None:
    """Clears the console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def view_product() -> None:
    """Display a product to the user"""
    prod_id = prompt_for_id()
    product = prod.get_product(prod_id)

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
    clear_screen()
    print('=' * 11)
    print('ADD PRODUCT')
    print('=' * 11, end='\n\n')

    product_name = prompt_for_product_name()
    product_quantity = prompt_for_int('Enter product quantity: ')
    product_price = prompt_for_int('Enter product price (cents): ')
    product_updated = datetime.now()

    product = {'product_name': product_name,
               'product_quantity': product_quantity,
               'product_price': product_price,
               'date_updated': product_updated}

    prod.add_product_to_db(product)

    input('\nProduct added to the database\n\nPress enter to continue...')


def create_backup() -> None:
    """Creates a backup"""
    products = prod.get_all_products()
    fieldnames = ['product_name', 'product_quantity', 'product_price', 'date_updated']
    
    with open('backup.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for product in products:
            writer.writerow({'product_name': product['product_name'],
                             'product_quantity': product['product_quantity'],
                             'product_price': product['product_price'],
                             'date_updated': product['date_updated'].strftime('%m/%d/%Y')})

    input('\nBackup has been created!\n\nPress enter to continue...')


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

