from django.utils import timezone
from django.db import connection
from django.db import models


# to add a default due time while creating a todo item
def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

#defining attribute of the list
class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_hence)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}: due {self.due_date}"
    
    class Meta:
        ordering = ["-due_date"]