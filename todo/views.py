from todo.models import Todo
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import TaskSerializer, TaskListSerializer
from rest_framework.permissions import IsAuthenticated


class HomeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        urls = {
            'List':'list/',
            'Detail':'detail/<int:id>',
            'Add':'add-task/',
            'Update':'update/task',
            'Delete':'delete-task/<int:id>',
        }
        return Response(urls)

# ApiView to retrieve all the task in the list and add a list item.
class TaskListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        TaskList = Todo.objects.all()
        serializer = TaskListSerializer(TaskList, many=True)
        if not TaskList:
            return Response({'msg': 'Task list is empty'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    def post(self, request, format=None):   
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ApiView to get, update, delete a list item.
class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id, format=None):
        try:
            task = Todo.objects.get(id=id)
            serialized = TaskSerializer(task)
            return Response(serialized.data)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, id, format=None):
        try:
            todo = Todo.objects.get(id=id)
            serializer = TaskSerializer(instance=todo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, id, format=None):
        try:
            task = Todo.objects.get(id=id)
            task.delete()
            return Response("Task is deleted successfully")
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

