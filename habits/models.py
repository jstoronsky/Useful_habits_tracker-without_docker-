from django.core.exceptions import ValidationError
from django.db import models
from users.models import NULLABLE
# Create your models here.
DAYS = 'days'
HOURS = 'hours'
MINUTES = 'minutes'
SECONDS = 'seconds'
MICROSECONDS = 'microseconds'

PERIOD_CHOICES = (
    (DAYS, 'Days'),
    (HOURS, 'Hours'),
    (MINUTES, 'Minutes'),
    (SECONDS, 'Seconds'),
    (MICROSECONDS, 'Microseconds'),
)


class UsefulHabit(models.Model):
    DAYS = DAYS
    HOURS = HOURS
    MINUTES = MINUTES
    SECONDS = SECONDS
    MICROSECONDS = MICROSECONDS

    PERIOD_CHOICES = PERIOD_CHOICES
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='создал привычку')
    place = models.CharField(max_length=150, verbose_name='место выполнения')
    time_to_start = models.TimeField(default='12:00:00', verbose_name='когда выполнять')
    time_to_end = models.TimeField(verbose_name='когда закончить выполнение')
    action = models.CharField(max_length=300, verbose_name='действие')
    linked_pleasant_habit = models.ForeignKey('PleasantHabit', on_delete=models.CASCADE,
                                              verbose_name='приятная привычка', **NULLABLE)
    interval = models.CharField(max_length=24, choices=PERIOD_CHOICES, verbose_name='периодичность выполнения')
    interval_value = models.IntegerField(verbose_name='числовое значение периодичности')
    reward = models.ForeignKey('Reward', on_delete=models.CASCADE, verbose_name='вознаграждение', **NULLABLE)
    is_public = models.BooleanField(verbose_name='привычка в открытом доступе?')

    def clean(self):
        if self.linked_pleasant_habit is not None and self.reward is not None:
            raise ValidationError('You can not set pleasant habit and reward simultaneously. '
                                  'Choose either first or second')

    class Meta:
        verbose_name = 'полезная привычка'
        verbose_name_plural = 'полезные привычки'


class PleasantHabit(models.Model):
    place = models.CharField(max_length=150, verbose_name='место выполнения привычки')
    time_to_start = models.TimeField(default='12:00:00', verbose_name='когда выполнять привычку')
    time_to_end = models.TimeField(verbose_name='когда закончить выполнение привычки')
    action = models.CharField(max_length=300, verbose_name='действие')

    class Meta:
        verbose_name = 'приятная привычка'
        verbose_name_plural = 'приятные привычки'


class Reward(models.Model):
    action = models.CharField(max_length=300, verbose_name='действие')

    class Meta:
        verbose_name = 'вознаграждение'
        verbose_name_plural = 'вознаграждения'
