from rest_framework import serializers
from habits.models import UsefulHabit, PleasantHabit, Reward
from habits.validators import HabitOrRewardValidator, TimeForHabitValidator


class PleasantHabitSerializer(serializers.ModelSerializer):
    """
    сериализатор для приятной привычки
    """
    class Meta:
        model = PleasantHabit
        fields = '__all__'


class RewardSerializer(serializers.ModelSerializer):
    """
    сериализатор для вознаграждения
    """
    class Meta:
        model = Reward
        fields = '__all__'


class UsefulHabitSerializer(serializers.ModelSerializer):
    """
    сериализатор для полезной привычки
    """
    pleasant_habit = PleasantHabitSerializer(required=False)
    reward = RewardSerializer(required=False)

    class Meta:
        model = UsefulHabit
        fields = '__all__'
        validators = [HabitOrRewardValidator(field1='pleasant_habit', field2='reward'),
                      TimeForHabitValidator(field='time_for_habit')]

    def create(self, validated_data):
        if 'pleasant_habit' in validated_data.keys():
            pleasant_habit_data = validated_data.pop('pleasant_habit')
            pleasant_habit = PleasantHabit.objects.create(**pleasant_habit_data)
            habit = UsefulHabit.objects.create(**validated_data, pleasant_habit=pleasant_habit)
            return habit
        elif 'reward' in validated_data.keys():
            reward_data = validated_data.pop('reward')
            reward = Reward.objects.create(**reward_data)
            habit = UsefulHabit.objects.create(**validated_data, reward=reward)
            return habit
        else:
            habit = UsefulHabit.objects.create(**validated_data)
            return habit

    def update(self, instance, validated_data):
        if 'pleasant_habit' in validated_data.keys():
            pleasant_habit_data = validated_data.pop('pleasant_habit')
            pleasant_habit = instance.pleasant_habit
            if pleasant_habit is None:
                PleasantHabit.objects.create(**pleasant_habit_data)
            else:
                pleasant_habit.action = pleasant_habit_data.get('action', pleasant_habit.action)
                pleasant_habit.place = pleasant_habit_data.get('place', pleasant_habit.place)
                if 'time_for_habit' in pleasant_habit_data.keys():
                    pleasant_habit.time_for_habit = pleasant_habit_data.get('time_for_habit',
                                                                            pleasant_habit.time_for_habit)
                pleasant_habit.save()

        elif 'reward' in validated_data.keys():
            reward_data = validated_data.pop('reward')
            reward = instance.reward
            if reward is None:
                Reward.objects.create(**reward_data)
            else:
                reward.action = reward_data.get('action', reward.action)
            reward.save()
        instance = super().update(instance, validated_data)

        return instance
