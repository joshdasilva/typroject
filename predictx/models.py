from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Stock(models.Model):
    stock_title = models.CharField(max_length=200)
    stock_name = models.TextField()
    #stock_link = models.TextField()
    #slug = models.SlugField(max_length=120)
    #favorite = models.ManyToManyField(User, related_name='favorite', blank=True)
    #stock_published = models.DateTimeField("date published", default=datetime.now())

def __str__(self):
    return self.stock_title
