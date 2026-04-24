from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from user.repository.home_repository import HomeRepository
from .repository import RoomRepository
from .serializer import RoomSerializer


class ListCreateRoomView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def get_queryset(self):
        method = self.request.method

        if method == "POST":
            return RoomRepository.get_all_rooms_in_home(self.request.user)

        return RoomRepository.get_all_available_rooms_for_user(self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        home = HomeRepository.get_home_by_user(user)
        serializer.save(home=home, user=user)


class RetrieveUpdateDestroyRoomView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def get_queryset(self):
        return RoomRepository.get_room_by_id(self.kwargs.get("pk"), self.request.user)
