from rest_framework import serializers
from .models import ToDoList

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ['id', 'title', 'due_date', 'created_date', 'completed']


