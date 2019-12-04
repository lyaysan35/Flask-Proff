
from peewee import *
import datetime

DATABASE = SqliteDatabase('professionals.sqlite')


# Create user class just like Dog App or TravelApp
class User(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    email = CharField()
    password = CharField()

    class Meta:
        database = DATABASE

class Professional(Model):
    # Strech goal -> Inherits from User -> meaning has all of User's fields plus the ones we add
    # created_at
    # email
    # password
    name = CharField()
    location = CharField()
    contact = CharField()
    bio = CharField()
    field = CharField()
    subfield = CharField()
    personal_image_url = CharField()
    # Has many images from foreign key on Image

    # field
    # subfield

    # Could query professionals who match a field

    class Meta:
        database = DATABASE
        

# class Field(Model):
#     name = CharField()
#     subfield = CharField()
#     created_at = DateTimeField(default=datetime.datetime.now)

#     class Meta:
#         database = DATABASE



class Image(Model):
    caption = CharField()
    url = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    # Belongs to professional -> Add a backref
    # professional.images = [Image1, Image2]
    professional = ForeignKeyField(Professional, backref='images')

    class Meta:
        database = DATABASE



class Rating(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    number = IntegerField() # 1 - 5
    review = TextField()

    # Many-to-Many relationship between user and professional
    # author = CharField() -> ForeignKey for User
    # professional = -> ForeignKey for Professional


    class Meta:
        database = DATABASE



def initialize():
    DATABASE.connect()
    # Update tables
    DATABASE.create_tables([User, Professional, Image, Rating], safe=True)
    print("TABLES Created")
    DATABASE.close()