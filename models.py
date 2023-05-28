# Models go here
import peewee

db = peewee.SqliteDatabase(":memory:")

class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    userid = peewee.AutoField()
    name = peewee.CharField(unique=True)
    address = peewee.CharField(max_length=300)
    billing_info = peewee.CharField(max_length=300)

    class Meta:
        table_name = 'users'

class Product(BaseModel):
    prodid = peewee.AutoField()
    name = peewee.CharField()
    owner = peewee.ForeignKeyField(User, column_name='user_id')
    description = peewee.CharField()
    price_per_unit_cents = peewee.BigIntegerField()
    amount_in_stock = peewee.IntegerField()

    class Meta:
        table_name = 'products'
        indexes=(('name'), True)

class Tag(BaseModel):
    product = peewee.ForeignKeyField(Product, column_name='product_id')
    number = peewee.IntegerField(column_name='tag_number')
    

class Transaction(BaseModel):
    transid = peewee.AutoField()
    product = peewee.ForeignKeyField(Product, column_name='product_id')
    buyer = peewee.ForeignKeyField(User, column_name='buyer=user_id')
    number_items = peewee.IntegerField()

    class Meta:
        table_name = 'transactions'

db.create_tables([User, Product, Tag, Transaction])


