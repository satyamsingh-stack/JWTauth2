from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=255, unique=True)
    email=models.EmailField(max_length=255, unique=True)
    password=models.CharField(max_length=255)

class Task(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    description=models.TextField()
    completed=models.BooleanField(default=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')