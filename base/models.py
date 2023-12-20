from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    
    id=models.TextField(primary_key=True)



    def __str__(self):
        return self.id
class Messages(models.Model):
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    created=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

class Participant(models.Model):
    users=models.ForeignKey(User,on_delete=models.CASCADE,related_name="users1")
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    def __int__(self):
        return self.id
    
