from rest_framework import serializers
from .models import Hotel, Floor, Room, IoTData

class HotelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class FloorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class IoTDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IoTData
        fields = '__all__'