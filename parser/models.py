from django.db import models

# Create your models here.
class Selector(models.Model):
    PLATFORM_CHOICES = [
        ('avito', 'Avito'),
        ('youla', 'Youla'),
        ('24au', '24au'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    search_box = models.CharField(max_length=255)
    search_button = models.CharField(max_length=255)
    next_button = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    link = models.CharField(max_length=255)