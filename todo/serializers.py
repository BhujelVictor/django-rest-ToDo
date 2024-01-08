from rest_framework import serializers
from .models import Todo

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'deadline', 'is_completed']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title','description', 'created_at', 'deadline', 'is_completed']


