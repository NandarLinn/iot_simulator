from rest_framework import viewsets, generics
from .models import Hotel, Floor, Room, IoTData
from .serializers import HotelSerializer, FloorSerializer, RoomSerializer, IoTDataSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

class HotelFloorsView(generics.ListAPIView):
    serializer_class = FloorSerializer

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Floor.objects.filter(hotel_id=hotel_id)
    
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
class FloorRoomsView(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        floor_id = self.kwargs.get('floor_id')
        return Room.objects.filter(floor_id=floor_id)

class IoTDataViewSet(viewsets.ModelViewSet):
    queryset = IoTData.objects.all()
    serializer_class = IoTDataSerializer

class RoomDataView(generics.ListAPIView):
    serializer_class = IoTDataSerializer

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        return IoTData.objects.filter(room_id=room_id)

class LifeBeingDataView(generics.ListAPIView):
    serializer_class = IoTDataSerializer

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        return IoTData.objects.filter(room_id=room_id, device_id='life_being')

class IAQDataView(generics.ListAPIView):
    serializer_class = IoTDataSerializer

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        return IoTData.objects.filter(room_id=room_id, device_id='iaq')