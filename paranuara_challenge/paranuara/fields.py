from decimal import Decimal

from django.db.models import QuerySet
from rest_framework import serializers


class BalanceField(serializers.CharField):
    """
    A Field to handle dollar sign string to decimal conversions
    """
    def to_internal_value(self, data):
        return Decimal(data.strip('$').replace(',',''))

    def to_representation(self, value):
        return f'${value}'


class StringListField(serializers.ListField):
    """
    A field to handle conversion between objects and a list of strings
    """
    child = serializers.CharField()

    def to_representation(self, data):
        if isinstance(data, QuerySet):
            return data.values_list('name', flat=True)
        elif isinstance(data, list):
            return data
        return data.all().values_list('name', flat=True)
