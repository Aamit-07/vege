from django.db import models

# Create your models here.

class Student(models.Model):
    # Id = models.AutoField()
    Name = models.CharField(max_length = 100)
    Age = models.IntegerField()
    Email = models.EmailField()
    Address = models.TextField()
