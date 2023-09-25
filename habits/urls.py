from habits.apps import HabitsConfig
from django.urls import path
from habits.views import CreateUsefulHabitAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('create/', CreateUsefulHabitAPIView.as_view(), name='habit_create')
]
