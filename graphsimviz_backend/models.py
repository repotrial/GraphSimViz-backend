from django.db import models


class ClusterTask(models.Model):
    UID = models.CharField(max_length=36, primary_key=True)
    request = models.TextField(unique=True)
    result = models.TextField(default='')
    error = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
