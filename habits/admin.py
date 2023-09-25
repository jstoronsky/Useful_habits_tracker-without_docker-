from django.contrib import admin
from habits.models import UsefulHabit, PleasantHabit, Reward
# Register your models here.


@admin.register(UsefulHabit)
class UsefulHabitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'action', 'place', 'user', 'time_to_start')


@admin.register(PleasantHabit)
class PleasantHabitAdmin(admin.ModelAdmin):
    list_display = ('place', 'action', 'time_to_start')


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('action',)
