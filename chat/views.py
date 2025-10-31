from datetime import timezone

from django.db import transaction
from django.db.models import OuterRef, Exists
from django.db.models.aggregates import Count
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from chat.models import RoomMember, Room, Message
from chat.serializers import RoomSearchSerializer, RoomSerializer, MessageSerializer, RoomMemberSerializer


# Create your views here.
class RoomSearchViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_membership = RoomMember.objects.filter(
            room=OuterRef('pk'),
            user=user
        )
        return Room.objects.annotate(
            is_member=Exists(user_membership)
        ).order_by('name')


class RoomListViewSet(ListModelMixin, GenericViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Room.objects.annotate(
            member_count=Count('memberships')
        ).filter(
            memberships__user_id=self.request.user.pk
        ).prefetch_related('last_message', 'last_message__user').order_by('-memberships__joined_at')


class MessageListCreateAPIView(ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        get_object_or_404(RoomMember, user=self.request.user, room_id=room_id)
        return Message.objects.filter(
            room_id=room_id).prefetch_related('user', 'room').order_by('-created_at')

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        room_id = self.kwargs['room_id']
        room = Room.objects.select_for_update().get(id=room_id)
        room.increment_version()
        channels = self.get_room_member_channels(room_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(room=room, user=request.user)
        room.last_message = obj
        room.bumped_at = timezone.now()
        room.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class JoinRoomView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, room_id):
        room = Room.objects.select_for_update().get(id=room_id)
        room.increment_version()
        if RoomMember.objects.filter(user=request.user, room=room).exists():
            return Response({"message": "already a member"}, status=status.HTTP_409_CONFLICT)
        obj, _ = RoomMember.objects.get_or_create(user=request.user, room=room)
        channels = self.get_room_member_channels(room_id)
        obj.room.member_count = len(channels)
        body = RoomMemberSerializer(obj).data
        return Response(body, status=status.HTTP_200_OK)



class LeaveRoomView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, room_id):
        room = Room.objects.select_for_update().get(id=room_id)
        room.increment_version()
        channels = self.get_room_member_channels(room_id)
        obj = get_object_or_404(RoomMember, user=request.user, room=room)
        obj.room.member_count = len(channels) - 1
        pk = obj.pk
        obj.delete()
        body = RoomMemberSerializer(obj).data
        return Response(body, status=status.HTTP_200_OK)


class RoomDetailViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        room = get_object_or_404(
            Room.objects.prefetch_related('memberships', 'last_message', 'last_message__user'),
            pk=pk
        )

        # Проверка: пользователь должен быть участником комнаты
        if not room.memberships.filter(user=request.user).exists():
            return Response({'detail': 'You are not a member of this room.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = RoomSerializer(room)
        return Response(serializer.data)
