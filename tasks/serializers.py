from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id') 
    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'description', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at') 

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status')

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status')
        read_only_fields = ('user', 'created_at', 'updated_at')