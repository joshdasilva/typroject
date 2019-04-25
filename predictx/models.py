from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Stock(models.Model):
    stock_title = models.CharField(max_length=200)
    stock_name = models.TextField()

def __str__(self):
    return self.stock_title
