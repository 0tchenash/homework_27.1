from django.db import models

# Create your models here.
class Ads(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    is_published = models.BooleanField()


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)