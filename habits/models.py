from datetime import timedelta
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import NULLABLE

# Create your models here.


class UsefulHabit(models.Model):
    """
    Модель полезной привычки. В методе clean определена дополнительная валидация, чтобы нельзя было нарушить логику
    приложения через админку.
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='создал привычку', **NULLABLE)
    place = models.CharField(max_length=150, verbose_name='место выполнения')
    time_to_start = models.TimeField(default='12:00:00', verbose_name='когда выполнять')
    time_for_habit = models.TimeField(default='00:02:00', verbose_name='время на выполнение привычки')
    action = models.CharField(max_length=300, verbose_name='действие')
    pleasant_habit = models.ForeignKey('PleasantHabit', on_delete=models.CASCADE,
                                       verbose_name='приятная привычка', **NULLABLE)
    interval_value = models.IntegerField(verbose_name='числовое значение периодичности',
                                         validators=[MaxValueValidator(7), MinValueValidator(1)])
    reward = models.ForeignKey('Reward', on_delete=models.CASCADE, verbose_name='вознаграждение', **NULLABLE)
    is_public = models.BooleanField(verbose_name='привычка в открытом доступе?')

    def clean(self):
        if self.pleasant_habit is not None and self.reward is not None:
            raise ValidationError('You can not set pleasant habit and reward simultaneously. '
                                  'Choose either first or second')

        elif timedelta(hours=self.time_for_habit.hour, minutes=self.time_for_habit.minute,
                       seconds=self.time_for_habit.second) > timedelta(seconds=120):
            raise ValidationError('This field can not be over 2 minutes')

    class Meta:
        verbose_name = 'полезная привычка'
        verbose_name_plural = 'полезные привычки'


class PleasantHabit(models.Model):
    """
    Модель приятной привычки
    """
    place = models.CharField(max_length=150, verbose_name='место выполнения привычки')
    time_for_habit = models.TimeField(default='00:02:00', verbose_name='время на выполнение привычки')
    action = models.CharField(max_length=300, verbose_name='действие')

    class Meta:
        verbose_name = 'приятная привычка'
        verbose_name_plural = 'приятные привычки'


class Reward(models.Model):
    """
    Модель вознаграждения
    """
    action = models.CharField(max_length=300, verbose_name='действие')

    class Meta:
        verbose_name = 'вознаграждение'
        verbose_name_plural = 'вознаграждения'
