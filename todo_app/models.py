from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class Todos(models.Model):
    PRIORITY_CHOICES = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    )

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    finished = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now, blank=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    due_date = models.DateTimeField(null=True, blank=True)
    public = models.BooleanField(default=False)
    files = models.ManyToManyField(UploadedFile, blank=True)

    def __str__(self):
        return self.title