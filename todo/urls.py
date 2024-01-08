from django.urls import path
from todo.views import HomeAPIView, TaskListView, TaskDetailView

urlpatterns = [
    path('', HomeAPIView.as_view(), name='home'),
    path('list/', TaskListView.as_view(), name='index'),
    path('add-task/', TaskListView.as_view(), name='add-task'),
    path('detail/<int:id>/', TaskDetailView.as_view(), name='detail'),
    path('update-task/<int:id>/', TaskDetailView.as_view(), name='update-task'),
    path('delete-task/<int:id>/', TaskDetailView.as_view(), name='delete-task'),
 
]