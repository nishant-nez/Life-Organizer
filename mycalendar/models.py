from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Events(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.CharField(max_length=255,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:  
        db_table = "tblevents"