from django.db import models

class Car(models.Model):
    title = models.CharField(max_length=150)
    descriptions = models.TextField()
    producer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    img = models.CharField(max_length=200)

