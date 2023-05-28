# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line

import models
from peewee import *
import re
import unique_names_generator 
from unique_names_generator import get_random_name
import random_address
import random
import string
from autocorrect import spell




def populate_test_database(number:int):
    user_data = []
    product_data = []
    tag_data = []
    transaction_data = []
    
    for i in range(number):

        rand_name = unique_names_generator.get_random_name()
        rand_address = random_address.real_random_address()   
        
        product_name = get_random_name()
        owner_id = random.randint(1, number)
        description = (''.join(random.choices(string.ascii_lowercase, k=5)))
        price_per_unit_cents = random.randint(1, 5000000)
        amount_in_stock = random.randint(0, 1000)

        product_id =random.randint(1, number)
        tag_number = random.randint(1000, 90000)

        buyer_id = random.randint(1, number)
        number_items = random.randint(1, 5)

        user_value = (rand_name, rand_address, rand_address)   
        user_data.append(user_value)

        product_value = (product_name, owner_id, description, price_per_unit_cents, amount_in_stock)
        product_data.append(product_value)

        tag_value = (product_id, tag_number)
        tag_data.append(tag_value)
        
        transaction_value = (product_id, buyer_id, number_items)
        transaction_data.append(transaction_value)
        
    user = models.User.insert_many(user_data, fields=[models.User.name, models.User.address, models.User.billing_info]).execute()
    product = models.Product.insert_many(product_data, fields=[models.Product.name, models.Product.owner, models.Product.description, models.Product.price_per_unit_cents, models.Product.amount_in_stock]).execute()
    tag = models.Tag.insert_many(tag_data, fields=[models.Tag.product, models.Tag.number]).execute()
    transaction = models.Transaction.insert_many(transaction_data, fields=[models.Transaction.product, models.Transaction.buyer, models.Transaction.number_items]).execute()

    return user, product, tag, transaction
    


def search(term):
    term = spell(term)
    products = []
    query = (models.Product.select())
    for product in query:
        if re.search(term, str(product.name), re.IGNORECASE) != None:
            products.append({product.prodid:product.name})
    return product



def list_user_products(user_id):
    products = []
    query = (models.Product.select(models.Product.name).where(models.Product.owner == user_id))
    for item in query:
        products.append(item.name)
    return products



def list_products_per_tag(tag_id):
    products = []
    query = (models.Product.select(models.Product.name).join(models.Tag).where(models.Tag.number == tag_id))
    for product in query:
        products.append(product)
    return products


def add_product_to_catalog(user_id, product):
    for item in models.Product.select():
        if item.name == product:
            return f'Product "{product}" exists and belongs to user with id {user_id}.'
        else:
            new_product = models.Product.create(name = product, owner = user_id, description = 'description', price_per_unit_cents = 2000, amount_in_stock = 2)
            return new_product.save()
            


          

def update_stock(product_id, new_quantity):
    query = (models.Product.select().where(models.Product.prodid == product_id))
    for item in query:
        item.amount_in_stock = new_quantity
        return item.save()
       


def purchase_product(product_id, buyer_id, quantity):

    q = (models.Product.select().where(models.Product.prodid == product_id))
    for item in q:
        if item.amount_in_stock >= quantity:
            transaction = models.Transaction.create(product = product_id, buyer = buyer_id, number_items = quantity)
            new_number = item.amount_in_stock - quantity  
            stock = update_stock(item.prodid, new_number)
            return transaction.save(), stock
        elif item.amount_in_stock < quantity:
            return f'You want to buy {quantity} items, but only {item.amount_in_stock} available.'
  
    


def remove_product(product_id):
    item = models.Product.get(models.Product.prodid == product_id)
    return item.delete_instance()



    



