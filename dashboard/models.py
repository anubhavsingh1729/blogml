from datetime import datetime
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.utils import timezone


class News(models.Model):
    headline = models.CharField(max_length = 250)
    text = models.TextField()
    author = models.CharField(max_length = 120)
    datemonth = models.CharField(max_length=50)
    def __str__(self):
        return self.headline
    objects = models.Manager

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    objects = models.Manager

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title