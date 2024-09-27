from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Todos(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) 
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000,blank=True)
    finished = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.title
