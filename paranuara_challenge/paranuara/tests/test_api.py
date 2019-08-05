from django.test import Client, TransactionTestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
from taggit.models import Tag

from paranuara_challenge.paranuara import views
from paranuara_challenge.paranuara.models import Company, Person, Food
from paranuara_challenge.paranuara.tests import testing_data


class TestSerializers(TransactionTestCase):


    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_endpoints(self):

        self.assertEqual(Company.objects.count(), 0)
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(Food.objects.count(), 0)

        crequest = self.factory.post(
            reverse('company-list'),
            testing_data.company_data,
            format='json'
        )
        cview = views.CompanyViewSet.as_view({'get': 'list', 'post': 'create'})
        cresponse = cview(crequest)
        assert cresponse.status_code == 200
        assert Company.objects.count() == 5

        # valid data
        prequest = self.factory.post(
            reverse('person-list'),
            testing_data.person_list_data,
            format='json'
        )
        pview = views.PersonViewSet.as_view({'get': 'list', 'post': 'create'})
        presponse = pview(prequest)
        assert presponse.status_code == 200
        assert Person.objects.count() == 6

        # invalid data
        pirequest = self.factory.post(
            reverse('person-list'),
            testing_data.invalid_data,
            format='json'
        )
        piview = views.PersonViewSet.as_view({'get': 'list', 'post': 'create'})
        piresponse = piview(pirequest)
        assert piresponse.status_code == 404


        # friends
        c = Client()
        response = c.get(
            reverse('friends', kwargs={'pk': 11, 'friend': 13})
        )
        assert response.status_code == 200

        # food
        response = c.get(
            reverse('food-list')
        )
        assert response.status_code == 200


        # assert related objects created
        assert Food.objects.count() == 8
        assert Tag.objects.count() == 31

