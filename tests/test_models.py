# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    #
    # ADD YOUR TEST CASES HERE
    #
        def test_read_product(self):
        """It should read a product from the database"""
        # Create a product
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        product.create()
        
        # Read the product from the database
        retrieved_product = Product.find(product.id)
        
        # Assert that the retrieved product matches the original product
        self.assertEqual(retrieved_product.id, product.id)
        self.assertEqual(retrieved_product.name, product.name)
        self.assertEqual(retrieved_product.description, product.description)
        self.assertEqual(retrieved_product.price, product.price)
        self.assertEqual(retrieved_product.available, product.available)
        self.assertEqual(retrieved_product.category, product.category)
        

    def test_update_product(self):
        """It should update a product in the database"""
        # Create a product
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        product.create()
        
        # Update the product
        product.name = "Updated Fedora"
        product.price = 15.75
        product.update()
        
        # Read the updated product from the database
        updated_product = Product.find(product.id)
        
        # Assert that the updated product matches the changes
        self.assertEqual(updated_product.id, product.id)
        self.assertEqual(updated_product.name, product.name)
        self.assertEqual(updated_product.price, product.price)


    def test_delete_product(self):
        """It should delete a product from the database"""
        # Create a product
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        product.create()
        
        # Delete the product from the database
        product.delete()
        
        # Attempt to retrieve the deleted product
        deleted_product = Product.find(product.id)
        
        # Assert that the deleted product is None
        self.assertIsNone(deleted_product)


    def test_list_all_products(self):
        """It should list all products from the database"""
        # Create some products
        Product(name="Hat", description="A nice hat", price=10.00, available=True, category=Category.CLOTHS).create()
        Product(name="Shirt", description="A cool shirt", price=20.00, available=True, category=Category.CLOTHS).create()
        
        # Get all products from the database
        products = Product.all()
        
        # Assert that there are two products
        self.assertEqual(len(products), 2)


    def test_search_product_by_name(self):
        """It should search for a product by name"""
        # Create a product
        Product(name="Hat", description="A nice hat", price=10.00, available=True, category=Category.CLOTHS).create()
        
        # Search for the product by name
        found_product = Product.find_by_name("Hat")
        
        # Assert that the found product matches the original product
        self.assertIsNotNone(found_product)
        self.assertEqual(found_product.name, "Hat")


    def test_search_product_by_category(self):
        """It should search for products by category"""
        # Create some products in the same category
        Product(name="Hat", description="A nice hat", price=10.00, available=True, category=Category.CLOTHS).create()
        Product(name="Shirt", description="A cool shirt", price=20.00, available=True, category=Category.CLOTHS).create()
        
        # Search for products in the category
        products = Product.find_by_category(Category.CLOTHS)
        
        # Assert that there are two products in the category
        self.assertEqual(len(products), 2)


    def test_search_product_by_availability(self):
        """It should search for products by availability"""
        # Create some products with different availability
        Product(name="Hat", description="A nice hat", price=10.00, available=True, category=Category.CLOTHS).create()
        Product(name="Shirt", description="A cool shirt", price=20.00, available=False, category=Category.CLOTHS).create()
        
        # Search for products by availability
        available_products = Product.find_by_availability(True)
        unavailable_products = Product.find_by_availability(False)
        
        # Assert that there is one available product and one unavailable product
        self.assertEqual(len(available_products), 1)
        self.assertEqual(len(unavailable_products), 1)
