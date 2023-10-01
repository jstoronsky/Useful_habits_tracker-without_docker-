from habits.apps import HabitsConfig
from django.urls import path
from habits.views import CreateUsefulHabitAPIView, UsefulHabitListAPIView, UsefulHabitRetrieveAPIView, \
    PrivateUsefulHabitsListAPIView, PrivateUsefulHabitRetrieveAPIView, UsefulHabitUpdateAPIView, \
    UsefulHabitDeleteAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('create/', CreateUsefulHabitAPIView.as_view(), name='habit_create'),
    path('list/', UsefulHabitListAPIView.as_view(), name='list_public_habits'),
    path('private/list/', PrivateUsefulHabitsListAPIView.as_view(), name='list_private_habits'),
    path('<int:pk>/', UsefulHabitRetrieveAPIView.as_view(), name='habit_detail'),
    path('private/<int:pk>/', PrivateUsefulHabitRetrieveAPIView.as_view(), name='private_habit_detail'),
    path('update/<int:pk>/', UsefulHabitUpdateAPIView.as_view(), name='habit_update'),
    path('delete/<int:pk>/', UsefulHabitDeleteAPIView.as_view(), name='habit_delete'),

    # path('pleasant/list/', PleasantHabitListAPIView.as_view(), name='list_pleasant_habits'),
    # path('pleasant/<int:pk>/', PleasantHabitRetrieveAPIView.as_view(), name='pleasant_habit_detail'),
    # path('pleasant/create/', PleasantHabitCreateAPIView.as_view(), name='pleasant_habit_create'),
    # path('pleasant/update/<int:pk>/', PleasantHabitUpdateAPIView.as_view(), name='pleasant_habit_update'),
    # path('pleasant/delete/<int:pk>/', PleasantHabitDeleteAPIView.as_view(), name='pleasant_habit_delete'),
    #
    # path('reward/list/', RewardListAPIView.as_view(), name='reward_list'),
    # path('reward/<int:pk>/', RewardRetrieveAPIView.as_view(), name='reward_detail'),
    # path('reward/create/', RewardCreateAPIView.as_view(), name='reward_create'),
    # path('reward/update/<int:pk>/', RewardUpdateAPIView.as_view(), name='reward_update'),
    # path('reward/delete/<int:pk>/', RewardDeleteAPIView.as_view(), name='reward_delete')
]
