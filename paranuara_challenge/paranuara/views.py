
from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response

from paranuara_challenge.paranuara.models import Company, Person, Food
from paranuara_challenge.paranuara.serializers import CompanySerializer, PersonSerializer, \
    FoodSerializer, CommonFriendsSerializer


#### COMPANIES ############################################

class CompanyViewSet(viewsets.ModelViewSet):
    """
    Company List and Detail view.

    Lists all Employees for a supplied Company by id.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_serializer(self, *args, **kwargs):
        """
        If a list is passed, set serializer to many.
        """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CompanyViewSet, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Company.objects.prefetch_related('employees')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Company.objects.all()
        output_serializer = CompanySerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)


#### FOOD ############################################

class FoodViewSet(viewsets.ModelViewSet):

    queryset = Food.objects.all()
    serializer_class = FoodSerializer


#### PEOPLE ############################################

class CommonFriendsViewSet(viewsets.ModelViewSet):
    """
    Given 2 People, provide name, age, address and phone
    along with any common living friends that have brown eyes.
    """

    queryset = Person.objects.all()
    serializer_class = CommonFriendsSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Check friends exist and provide person and friend to serializer
        """
        try:
            person = Person.objects.get(id=kwargs.get('pk'))
            friend = Person.objects.get(id=kwargs.get('friend'))
        except Person.DoesNotExist:
            raise Http404

        person.friend = friend
        self.object = person

        serializer = CommonFriendsSerializer(
            person,
            self.get_serializer_context()
        )
        serializer.is_valid()
        return Response(serializer.data)


class PersonViewSet(viewsets.ModelViewSet):

    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get_serializer(self, *args, **kwargs):
        """
        If a list is passed, set serializer to many.
        """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(PersonViewSet, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Person.objects.prefetch_related(
            'friends', # 'food', 'tags'
        ).select_related('company')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Person.objects.all()
        output_serializer = PersonSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)
