from django.shortcuts import render
from rest_framework import generics
from habits.models import UsefulHabit
from habits.serializers import UsefulHabitSerializer
# Create your views here.


class CreateUsefulHabitAPIView(generics.CreateAPIView):
    serializer_class = UsefulHabitSerializer
