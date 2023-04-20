from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class TodoSerializer(serializers.ModelSerializer):
    #CASCADE: When the referenced object is deleted, also delete the objects that have references to it
    #(when you remove a blog post for instance, you might want to delete comments as well).
    #models.restrict is dont allow to delete
    user=serializers.CharField(source='user.username',read_only=True)#read only means we cannot insert
    class Meta:
        model=Task
        fields=('__all__')
        read_only_fields=('user',)
    def create(self,validated_data):
        validated_data['user']=self.context['request'].user
        return Task.objects.create(**validated_data)
    