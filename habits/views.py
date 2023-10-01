from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from habits.models import UsefulHabit
from habits.serializers import UsefulHabitSerializer
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
# Create your views here.


class CreateUsefulHabitAPIView(generics.CreateAPIView):
    """
    эндпоинт для создания полезной привычки
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UsefulHabitSerializer


class UsefulHabitListAPIView(generics.ListAPIView):
    """
    эндпоинт для спиского отображения полезных привычек, которые являются публичными
    """
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.filter(is_public=True)


class UsefulHabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    эндпоинт для отображения полезной привычки, которая является публичной
    """
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.filter(is_public=True)


class PrivateUsefulHabitsListAPIView(generics.ListAPIView):
    """
    эндпоинт, через который пользователь запрашивает списковое отображение своих привычек.
    Требуется авторизация
    """
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator
    serializer_class = UsefulHabitSerializer

    def get_queryset(self):
        user = self.request.user
        return UsefulHabit.objects.filter(user=user)


class PrivateUsefulHabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    эндпоинт через который пользователь запрашивает отображение своей конкретной привычки.
    Требуется авторизация
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UsefulHabitSerializer

    def get_queryset(self):
        user = self.request.user
        return UsefulHabit.objects.filter(user=user)


class UsefulHabitUpdateAPIView(generics.UpdateAPIView):
    """
    эндпоинт для обновления привычки
    """
    permission_classes = [IsAuthenticated | IsOwner]
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.all()


class UsefulHabitDeleteAPIView(generics.DestroyAPIView):
    """
    эндпоинт для удаления полезной привычки и связанной с ней приятной привычки или вознаграждения
    """
    permission_classes = [IsAuthenticated | IsOwner]
    queryset = UsefulHabit.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.reward is not None:
            instance.reward.delete()
        elif instance.pleasant_habit is not None:
            instance.pleasant_habit.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class PleasantHabitListAPIView(generics.ListAPIView):
#     serializer_class = PleasantHabitSerializer
#     queryset = PleasantHabit.objects.all()
#
#
# class PleasantHabitRetrieveAPIView(generics.RetrieveAPIView):
#     serializer_class = PleasantHabitSerializer
#     queryset = PleasantHabit.objects.all()
#
#
# class PleasantHabitCreateAPIView(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PleasantHabitSerializer
#
#
# class PleasantHabitUpdateAPIView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated | IsOwnerSetVariant]
#     serializer_class = PleasantHabitSerializer
#     queryset = PleasantHabit.objects.all()
#
#
# class PleasantHabitDeleteAPIView(generics.DestroyAPIView):
#     permission_classes = [IsAuthenticated | IsOwnerSetVariant]
#     queryset = PleasantHabit.objects.all()
#
#
# class RewardListAPIView(generics.ListAPIView):
#     serializer_class = RewardSerializer
#     queryset = Reward.objects.all()
#
#
# class RewardRetrieveAPIView(generics.RetrieveAPIView):
#     serializer_class = RewardSerializer
#     queryset = Reward.objects.all()
#
#
# class RewardCreateAPIView(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = RewardSerializer
#
#
# class RewardUpdateAPIView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated | IsOwnerSetVariant]
#     serializer_class = RewardSerializer
#     queryset = Reward.objects.all()
#
#
# class RewardDeleteAPIView(generics.DestroyAPIView):
#     permission_classes = [IsAuthenticated | IsOwnerSetVariant]
#     queryset = Reward.objects.all()
