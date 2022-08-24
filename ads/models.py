from django.db import models
from users.models import User

# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

class Ad(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    price = models.IntegerField()
    description = models.TextField()
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='images/', default=None, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['name']