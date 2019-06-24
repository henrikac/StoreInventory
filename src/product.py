"""Contains all database related stuff

Type hints were not added to this file
because peewee does not support type hinting
"""

from datetime import datetime

from peewee import *
from playhouse.shortcuts import model_to_dict


db = SqliteDatabase('inventory.db')


def open_db():
    """Opens the database connection and creates the tables"""
    db.connect()
    db.create_tables([Product], safe=True)


def close_db():
    """Closes the database connection"""
    db.close()


def add_products_to_db(products):
    """Adds products to the database.
    If a 'product_name' already exists in the database
    the most recent updated version will be saved to the database
    """
    with db.atomic():
        for product in products:
            try:
                Product.create(**product)
            except IntegrityError:
                old_product = Product.get(product_name=product['product_name'])

                if old_product.date_updated < product['date_updated']:
                    old_product.product_price = product['product_price']
                    old_product.product_quantity = product['product_quantity']
                    old_product.date_updated = product['date_updated']
                    old_product.save()


def get_product(id):
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

