from decimal import Decimal

from django.test import TestCase

from paranuara_challenge.paranuara import helpers
from paranuara_challenge.paranuara.helpers import FOOD_CLASSIFICATION_CHOICES
from paranuara_challenge.paranuara.models import Person, Company, Food, GENDER_CHOICES

class PersonTestCase(TestCase):

    def setUp(self) -> None:
        c1 = Company.objects.create(
            name='ERTHLNGS',
        )
        c2 = Company.objects.create(
            name='PARALINGS',
        )
        c3 = Company.objects.create(
            name='MOONLINGS',
        )

        Food.objects.create(
            name='grapefruit',
        )

        Person.objects.create(
            _id = 'hgjdksangdsafdklsaf1',
            id = 1,
            name = 'Timmy Testuser',
            email = 'timmy@paranuara.com',
            eye_color = 'brown',
            balance=Decimal('93.00'),
            gender = GENDER_CHOICES.male,
            has_died = False,
            age = 18,
            company = c1,
            _friend_cache = [
                {'id': 2},
                {'id': 4},
                {'id': 5},
            ]
        )
        Person.objects.create(
            _id = 'hgjdksanfdsafdklsaf2',
            id = 2,
            name = 'Terri Testuser',
            email = 'terri@paranuara.com',
            eye_color = 'brown',
            gender = GENDER_CHOICES.female,
            has_died = False,
            balance=Decimal('193.00'),
            age = 54,
            company = c2,
            _friend_cache = [
                {'id': 1},
                {'id': 3},
                {'id': 5},
            ]
        )
        Person.objects.create(
            _id = 'hgjddsangdsafdklsaf3',
            id = 3,
            name = 'Tommy Testuser',
            email = 'tommy@paranuara.com',
            eye_color = 'grey',
            gender = GENDER_CHOICES.male,
            has_died = False,
            balance=Decimal('930.00'),
            age = 37,
            company = c1,
            _friend_cache = [
                {'id': 6},
                {'id': 2},
                {'id': 4},
                {'id': 5},
            ]
        )
        Person.objects.create(
            _id = 'hgjdksangdsaffdsfs14',
            id = 4,
            name = 'Tammy Testuser',
            email = 'tammy@paranuara.com',
            eye_color = 'blue',
            gender = GENDER_CHOICES.female,
            has_died = True,
            balance=Decimal('3393.00'),
            age = 83,
            company = c3,
            _friend_cache = [
                {'id': 1},
                {'id': 6},
                {'id': 5},
            ]
        )
        Person.objects.create(
            _id = 'hgjdksangdsaffdsfs15',
            id = 5,
            name = 'Cody Testuser',
            email = 'cody@paranuara.com',
            eye_color = 'brown',
            gender = GENDER_CHOICES.male,
            has_died = True,
            balance=Decimal('903.00'),
            age = 23,
            company = c2,
            _friend_cache = [
                {'id': 2},
                {'id': 3},
                {'id': 4},
            ]
        )
        Person.objects.create(
            _id = 'hgjdksangdsaffdsfs15',
            id = 6,
            name = 'Kerri Testuser',
            email = 'kerri@paranuara.com',
            eye_color = 'brown',
            gender = GENDER_CHOICES.female,
            has_died = False,
            balance=Decimal('935.00'),
            age = 29,
            company = c2,
            _friend_cache = [
                {'id': 2},
                {'id': 5},
                {'id': 4},
                {'id': 3},
            ]
        )

    def test_update_friends(self):

        p1 = Person.objects.get(id=1)

        p1.update_friends()
        p1_cache = [f['id'] for f in p1._friend_cache].sort()
        p1_friends = list(p1.friends.all().values_list(flat=True)).sort()
        self.assertEqual(p1_cache, p1_friends)

    def test_get_balance(self):

        p1 = Person.objects.get(id=1)
        p2 = Person.objects.get(id=2)
        p3 = Person.objects.get(id=3)

        bal = p1.get_balance()
        self.assertEqual(bal, f'${p1.balance}')


    def test_str(self):
        p1 = Person.objects.get(id=1)
        self.assertEqual(p1.__str__(), p1.name)

        c1 = Company.objects.get(name='ERTHLNGS')
        self.assertEqual(c1.__str__(), c1.name)

        f1 = Food.objects.get(name='grapefruit')
        self.assertEqual(f1.name, f1.__str__())

    def test_food_classification(self):
        # check unknown food type (not str)

        fx = 45
        rr = helpers.check_food_classification(fx)
        self.assertEqual(rr, 'x')

        known = 'apple'
        rr = helpers.check_food_classification(known)
        self.assertEqual(rr, FOOD_CLASSIFICATION_CHOICES.fruit)

        known = 'carrot'
        rr = helpers.check_food_classification(known)
        self.assertEqual(rr, FOOD_CLASSIFICATION_CHOICES.vegetable)

