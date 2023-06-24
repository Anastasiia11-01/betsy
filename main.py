# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line

import models
from peewee import *
import re
import unique_names_generator 
import random_address
import random
import string
from textblob import TextBlob
from autocorrect import Speller
import os

def main():
    populate_test_database(50)
    search('shirt')
    list_user_products(1)
    list_products_per_tag(2)
    add_product_to_catalog(1, 'shirt')
    update_stock(1, 5)
    purchase_product(1, 1, 1)
    remove_product(1)

"""new_product1 = models.Product.create(name = 'product', owner = 2, description = 'description', price_per_unit_cents = 2000, amount_in_stock = 2)
print(new_product1.prodid) """          

#creates and populates a database based on models.py
def populate_test_database(number:int):
    
    os.getcwd()
   
    user_data = []
    product_data = []
    tag_data = []
    transaction_data = []
    
    for i in range(number):

        rand_name = unique_names_generator.get_random_name()
        rand_address = random_address.real_random_address()   
        

        product_list = ['tv','shirt', 'couch', 'sofa', ' trousers', 'baby clothing', 'buggy', 'bike', 'car', 'table', 'chair', 'phone', 'mobile', 'tiger', 'print', 'cow']
        product_name = random.choice(product_list)
        owner_id = random.randint(1, number)
        description = (''.join(random.choices(string.ascii_lowercase, k=5)))
        price_per_unit_cents = random.randint(1, 5000000)
        amount_in_stock = random.randint(0, 1000)

        product_id =random.randint(1, number)
        tag_number = random.randint(1, number)

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

    

print(populate_test_database(50))


# returns a list of products with their ids, which consist a given term in their name.
def search(term):
    final_term = TextBlob(term)
    products = []
    query = (models.Product.select())
    for product in query:
        if re.search(str(final_term.correct()), str(product.name), re.IGNORECASE) != None:
            products.append({product.prodid:product.name})
    return products
    


#print(search('chirt'))

#returns list of products sold by a given user.
def list_user_products(user_id):
    products = []
    query = (models.Product.select(models.Product.name).where(models.Product.owner == user_id))
    for item in query:
        products.append(item.name)
    return products

#print(list_user_products(45))


#returns list of products with the given tag.
def list_products_per_tag(tag_number):
    products = []
    query = (models.Product.select(models.Product.name).join(models.Tag).where(models.Tag.number == tag_number))
    for product in query:
        products.append(product)
    return products

#print(list_products_per_tag(10))

#adds new product to a catalog.
def add_product_to_catalog(user_id, product):
    for item in models.Product.select():
        if item.name == product:
            return f'Product "{product}" exists and belongs to user with id {user_id}.'
        else:
            new_product = models.Product.create(name = product, owner = user_id, description = 'description', price_per_unit_cents = 2000, amount_in_stock = 2)
            return new_product.save()
            

#print(add_product_to_catalog(50, 'joke'))
          
#updates quantity of a given product to a given number.
def update_stock(product_id, new_quantity):
    query = (models.Product.select().where(models.Product.prodid == product_id))
    for item in query:
        item.amount_in_stock = new_quantity
        return item.save()
    
#print(update_stock(2, 8))
     
       
"""print(update_stock(1, 4))
print(new_product1.amount_in_stock)"""


#creates a new transaction for a given number of products to a given buyer 
# or notifies if there are not enough items in stock.
def purchase_product(product_id, buyer_id, quantity):

    q = (models.Product.select().where(models.Product.prodid == product_id))
    for item in q:
        if item.amount_in_stock >= quantity:
            transaction = models.Transaction.create(product = product_id, buyer = buyer_id, number_items = quantity)
            new_number = item.amount_in_stock - quantity  
            stock = update_stock(item.prodid, new_number)
            transaction.save()
            return f'Products successfully purchased. Remaining amount of itmes in stock: {stock}' 
        elif item.amount_in_stock < quantity:
            return f'You want to buy {quantity} items, but only {item.amount_in_stock} available.'
  
#print(purchase_product(10, 1, 2000000))    

#deletes a given product form the database.
def remove_product(product_id):
    item = models.Product.get(models.Product.prodid == product_id)
    item.delete_instance()
    return f'The item removed.'

#print(remove_product(2))

if __name__=='__main__':
    main()



    







    



