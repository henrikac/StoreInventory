import csv
from datetime import datetime
import os
import unittest

from app import clean_data, convert_data, read_csv


class TestDataFunctions(unittest.TestCase):
    def setUp(self):
        self.tmp_data = [{'product_name': 'Milk', 'product_quantity': '32',
                     'product_price': '$8.99', 'date_updated': '1/06/2019'},
                    {'product_name': 'Oranges', 'product_quantity': '52',
                     'product_price': '$1.72', 'date_updated': '12/27/2018'},
                    {'product_name': 'Cream', 'product_quantity': '12',
                     'product_price': '$4.32', 'date_updated': '06/23/2019'}]
        self.csv_file = 'tmp_data.csv'

        if not os.path.isfile(self.csv_file):
            with open(self.csv_file, 'w') as csvfile:
                fieldnames = ['product_name',
                              'product_quantity',
                              'product_price',
                              'date_updated']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for data in self.tmp_data:
                    writer.writerow(data)

    def tearDown(self):
        if os.path.isfile(self.csv_file):
            os.remove(self.csv_file)

    def test_read_csv(self):
        self.assertEqual(len(read_csv(self.csv_file)), 3)

    def test_convert_data(self):
        product = convert_data(self.tmp_data[0])

        self.assertTrue(isinstance(product['product_name'], str))
        self.assertTrue(isinstance(product['product_quantity'], int))
        self.assertTrue(isinstance(product['product_price'], int))
        self.assertTrue(isinstance(product['date_updated'], datetime))

    def test_clean_data(self):
        data = read_csv(self.csv_file)
        cleaned_data = clean_data(data)

        for product in self.tmp_data:
            product = convert_data(product)

        self.assertEqual(self.tmp_data, cleaned_data)
                


if __name__ == '__main__':
    unittest.main()

