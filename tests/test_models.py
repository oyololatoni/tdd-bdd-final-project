Here are the test cases for the mentioned scenarios:

```python
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
```
