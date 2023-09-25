from rest_framework import serializers
from habits.models import UsefulHabit
from habits.validators import HabitOrRewardValidator


class UsefulHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsefulHabit
        fields = '__all__'
        validators = [HabitOrRewardValidator(field1='linked_pleasant_habit', field2='reward')]
