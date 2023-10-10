from django.db import models

# Create your models here.
"""
I assume that hotel doesn't have other branches.
Each htotel has 3 floors and each floor has 10 rooms.
"""

# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=100)

class Floor(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    number = models.IntegerField()

class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)

class IoTData(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    device_id = models.CharField(max_length=20)
    datapoint = models.CharField(max_length=20)
    value = models.CharField(max_length=20)