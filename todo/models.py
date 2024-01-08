from django.utils import timezone
from django.db import models


# to add a default due time while creating a todo item
def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

#defining attribute of the list
class Todo(models.Model):
    title = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(default=one_week_hence)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}: due {self.deadline}"
    
    class Meta:
        ordering = ["-deadline"]