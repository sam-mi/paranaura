from rest_framework import serializers
from rest_framework.exceptions import NotFound
from taggit.models import Tag

from paranuara_challenge.paranuara.fields import BalanceField, StringListField
from paranuara_challenge.paranuara.helpers import check_food_classification
from paranuara_challenge.paranuara.models import Person, Company, Food


#### COMPANIES ############################################


class CompanySerializer(serializers.ModelSerializer):
    """
    Create and view Company models
    """
    index = serializers.IntegerField(source='id')
    company = serializers.CharField(source='name')

    def create(self, validated_data):
        company, action = Company.objects.update_or_create(**validated_data)
        return company

    employees = serializers.SerializerMethodField(read_only=True)
    def get_employees(self, value):
        if isinstance(value, Company) :
            return PersonIndexSerializer(value.employees.all(), many=True).data
        return []

    class Meta:
        model = Company
        fields = (
            'index', 'company', 'employees', 'created'
        )
        read_only_fields = ('created',)


#### FOOD ############################################


class FoodSerializer(serializers.ModelSerializer):

    classification = serializers.SerializerMethodField()

    def get_classification(self, value):
        return value.get_classification_display().lower()

    class Meta:
        model = Food
        fields = (
            'name', 'classification'
        )


#### TAGS ############################################


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'name',
        )


#### PEOPLE ############################################


class PersonIndexSerializer(serializers.ModelSerializer):
    """
    List friends for a Person
    """

    index = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = Person
        fields = (
            'index',
        )
        read_only_fields = fields


class FriendComparisonSerializer(serializers.ModelSerializer):

    index = serializers.IntegerField(source='id')
    eyeColor = serializers.CharField(source='eye_color')

    class Meta:
        model = Person
        fields = (
            'index', 'guid', 'eyeColor',
            'name', 'age', 'address', 'phone'
        )
        read_only_fields = fields


class CommonFriendsSerializer(serializers.ModelSerializer):
    """
    Given 2 People, provide name, age, address and phone
    along with any common living friends that have brown eyes.
    """

    person = serializers.SerializerMethodField()
    friend = serializers.SerializerMethodField()
    common_friends = serializers.SerializerMethodField('get_common_friends')

    def get_person(self, value):
        return FriendComparisonSerializer(value).data

    def get_friend(self, value):
        return FriendComparisonSerializer(value.friend).data

    def get_common_friends(self, value):
        friend = value.friend
        friend.update_friends()
        value.update_friends()
        ids = [value.id, friend.id]
        common_friends = Person.objects.filter(
            friends__id__in=ids, eye_color='brown', has_died=False
        )
        return FriendComparisonSerializer(common_friends, many=True).data


    class Meta:
        model = Person
        fields = (
            'person', 'friend', 'common_friends',
        )


class PersonSerializer(PersonIndexSerializer):
    """
    A Serializer for the Person model,

    allows for single and multiple assignments as well as
    updating via POST.
    """

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(PersonSerializer, self).__init__(many=many, *args, **kwargs)

    eyeColor = serializers.CharField(source='eye_color')
    has_died = serializers.BooleanField(required=True)

    friends = PersonIndexSerializer(many=True)
    _friend_cache = serializers.JSONField(required=False, write_only=True)

    tags = StringListField(
        required=False,
    )
    favouriteFood = StringListField(
        source='food',
        required=False,
    )
    balance = BalanceField()
    company_id = serializers.PrimaryKeyRelatedField(
        required=False,
        source='company',
        queryset=Company.objects.all(),
    )
    registered = serializers.DateTimeField(
        format='%Y-%m-%dT%H:%M:%S %z',
        input_formats=['%Y-%m-%dT%H:%M:%S %z']
    )

    def create(self, validated_data):

        friends = validated_data.pop('friends', [])

        food = validated_data.pop('food', [])
        foods = []
        if food:
            for name in food:
                item, c = Food.objects.get_or_create(
                    name=name,
                )
                item.classification = check_food_classification(name)
                item.save()
                foods.append(item)

        tags = validated_data.pop('tags', [])
        _tags = []
        if tags:
            for tag in tags:
                item, c = Tag.objects.get_or_create(name=tag)
                _tags.append(item)

        person, c = Person.objects.update_or_create(**validated_data)
        person._friend_cache = friends
        person.save()

        person.food.add(*foods)
        person.tags.add(*_tags)

        # add m2m friends that exist
        person.update_friends()
        person.save()
        return person


    def to_internal_value(self, data):
        if data.get('company_id'):
            try:
                company = Company.objects.get(id=data['company_id'])
            except Company.DoesNotExist:
                raise NotFound(
                    f"Company with id: {data['company_id']} does not exist. A Company "
                    f"record must exist before creating a Person with a relation "
                    f"to it, failing row id: {data['index']}. "
                )
        return super().to_internal_value(data)


    class Meta:
        model = Person
        fields = (
            'guid', '_id', 'index', 'name', 'email', 'address', 'company_id',
            'friends', '_friend_cache', 'favouriteFood', 'registered',
            'gender', 'age', 'picture', 'tags', 'greeting', 'phone', 'eyeColor',
            'balance', 'has_died', 'about'
        )
        read_only_fields = ('created', 'food')
        write_only_fields = ('password', 'confirm_password', '_friend_cache')
