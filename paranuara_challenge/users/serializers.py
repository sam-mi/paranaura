from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import User


__author__ = 'pure'
__created__ = '21/09/2014'
__copyright__ = 'Copyright (C) 2014 PureCreative'



class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)



class UserSerializer(serializers.HyperlinkedModelSerializer):
    #votes = serializers.HyperlinkedRelatedField(many=True, view_name="users-list", lookup_field="username")
    #permissions = serializers.HyperlinkedRelatedField(many=True, view_name='permission-detail')

    profile = UserProfileSerializer(read_only=True)
    permissions = serializers.ReadOnlyField(source='get_all_permissions')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'groups', 'url',
            'salutation', 'name', 'permissions',
            'date_joined', 'profile'
        )
        read_only_fields = ('date_joined',)
        write_only_fields = ('password', 'confirm_password')
