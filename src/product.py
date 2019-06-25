"""Contains all database related stuff

Running 'mypy' on this file will cause lots errors
because peewee doesn't support type hints

Created: 2019
Author: Henrik A. Christensen
"""

from datetime import datetime
from typing import Dict, List, Union

from peewee import *
from playhouse.shortcuts import model_to_dict


db = SqliteDatabase('inventory.db')


def open_db() -> None:
    """Opens the database connection and creates the tables"""
    db.connect()
    db.create_tables([Product], safe=True)


def close_db() -> None:
    """Closes the database connection"""
    db.close()


def add_products_to_db(products: List[Dict]) -> None:
    """Adds a list of products to the database.
    If a 'product_name' already exists in the database
    the most recent updated version will be saved to the database
    """
    with db.atomic():
        for product in products:
            add_product_to_db(product)


def add_product_to_db(product: Dict) -> None:
    """Adds a single product to the database
    If a 'product_name' already exists in the database
    the most recent updated version wil be saved to the database
    """
    try:
        Product.create(**product)
    except IntegrityError:
        old_product = Product.get(product_name=product['product_name'])

        if old_product.date_updated <= product['date_updated']:
            old_product.product_price = product['product_price']
            old_product.product_quantity = product['product_quantity']
            old_product.date_updated = product['date_updated']
            old_product.save()


def get_all_products() -> List[Dict]:
    """Gets all the products and transforms them into dicts"""
    products = Product.select()
    products_dict: List[Dict] = []

    for product in products:
        products_dict.append(model_to_dict(product))

    return products_dict


def get_product(id: int) -> Union[Dict, None]:
    """Gets a product from the database by its id
    Returns None if no product with given id
    """
    product = Product.get_or_none(Product.product_id == id)

    if product:
        return model_to_dict(product)

    return product


class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length=140, unique=True)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField(default=datetime.now)

    class Meta:
        database = db

    def __str__(self):
        return self.product_name

