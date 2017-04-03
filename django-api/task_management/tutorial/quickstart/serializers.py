from django.contrib.auth.models import User, Group
from tutorial.quickstart.models import task_table
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class taskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = task_table
        fields = ('url', 'title', 'status', 'admin', 'assignee')
    # def create(self, validated_data):
    #     return task.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.admin_id = validated_data.get('admin_id', instance.admin_id)
    #     instance.save()
    #     return instance