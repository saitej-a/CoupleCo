from django.contrib import admin
from .models import Room,Messages,Participant

# Register your models here.
admin.site.register(Room)
admin.site.register(Messages)
admin.site.register(Participant)