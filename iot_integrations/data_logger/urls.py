from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, HotelFloorsView, FloorViewSet, RoomViewSet, IoTDataViewSet, FloorRoomsView, RoomDataView, LifeBeingDataView, IAQDataView
from django.urls import path, include

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'floors', FloorViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'data', IoTDataViewSet)


urlpatterns = router.urls
urlpatterns += [path('hotels/<int:hotel_id>/floors/', HotelFloorsView.as_view(), name='hotel-floors'),
                path('floors/<int:floor_id>/rooms/', FloorRoomsView.as_view(), name='floor-rooms'),
                path('rooms/<int:room_id>/data/', RoomDataView.as_view(), name='room-data'),
                path('rooms/<int:room_id>/life_being/', LifeBeingDataView.as_view(), name='room-life_being'),
                path('rooms/<int:room_id>/iaq/', IAQDataView.as_view(), name='room-iaq'),]