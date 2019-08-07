from django.db import models
from factory import DjangoModelFactory, Faker
from faker import Factory

from paranuara_challenge.paranuara.models import Company, Food, Person

faker = Factory.create()

class CompanyFactory(DjangoModelFactory):
    name = Faker('company')

    class Meta:
        model = Company


class FoodFactory(DjangoModelFactory):
    name = Faker('food')
    # category = Faker('sentence')

    class Meta:
        model = Food


class PersonFactory(DjangoModelFactory):
    # _id = faker.pystr(max_chars=24, min_chars=20)
    # id = faker.,
    # name = faker.name()
    # email = 'timmy@paranuara.com',
    # eye_color = 'brown',
    # balance = Decimal('93.00'),
    # gender = faker.st,
    # has_died = False,
    # age = 18,
    # company = c1,
    # _friend_cache = [
    #     {'id': 2},
    #     {'id': 4},
    #     {'id': 5},
    # ]

    class Meta:
        model = Person
