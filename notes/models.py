from django.db import models
from django.contrib.auth.models import User

class Notes(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=50000,blank=True)
    dateedited = models.DateTimeField(auto_now=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title