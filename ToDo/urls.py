from django.urls import path
from ToDo.views import HomeAPIView, TaskListView, TaskDetailView, TaskAddView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('', HomeAPIView.as_view(), name='home'),
    path('list/', TaskListView.as_view(), name='index'),
    path('detail/<int:id>/', TaskDetailView.as_view(), name='detail'),
    path('add-task/', TaskAddView.as_view(), name='add-task'),
    path('update-task/<int:id>/', TaskUpdateView.as_view(), name='update-task'),
    path('delete-task/<int:id>/', TaskDeleteView.as_view(), name='delete-task'),
 
]