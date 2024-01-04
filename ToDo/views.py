from ToDo.models import ToDoList
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status
from .serializers import TaskSerializer

class HomeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        urls = {
            'List':'list/',
            'Detail':'detail/<int:id>',
            'Add':'add-task/',
            'Update':'update/task',
            'Delete':'delete-task/<int:id>',
        }
        return Response(urls)

class TaskListView(APIView):
    """
    List all tasks.
    """
    def get(self, request, format=None):
        TaskList = ToDoList.objects.all()
        serializer = TaskSerializer(TaskList, many=True)
        return Response(serializer.data)

class TaskAddView(APIView):
    """
    Create a new task
    """
    def post(self, request, format=None):   
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    """
    Retrieve a task instance.
    """
    def get(self, request, id, format=None):
        try:
            task = ToDoList.objects.get(id=id)
            serialized = TaskSerializer(task)
            return Response(serialized.data)
        except ToDoList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
class TaskUpdateView(APIView):
    """
    Update a task instance.
    """
    def put(self, request, id, format=None):
        try:
            todo = ToDoList.objects.get(id=id)
            serializer = TaskSerializer(instance=todo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ToDoList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class TaskDeleteView(APIView):
    """
    Delete a task instance.
    """
    def delete(self, request, id, format=None):
        try:
            task = ToDoList.objects.get(id=id)
            task.delete()
            return Response("Task is deleted successfully")
        except ToDoList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

