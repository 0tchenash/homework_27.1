from django.db import models

# Create your models here.
class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"
        ordering = ['name']

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    age = models.IntegerField()
    role = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']