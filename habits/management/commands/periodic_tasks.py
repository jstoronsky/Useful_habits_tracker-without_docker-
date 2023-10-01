import os
from datetime import datetime, timedelta
import pytz
from django.core.management import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from habits.models import UsefulHabit

utc = pytz.UTC


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.join('habits', 'tasks.py')
        with open(path, 'r+') as file:
            line = file.readline()
            while line:
                if line.rstrip() == 'habits = UsefulHabit.objects.all()':
                    file.truncate(file.tell())
                    break
                line = file.readline()

        PeriodicTask.objects.all().delete()
        IntervalSchedule.objects.all().delete()
        habits = UsefulHabit.objects.all()
        for habit in habits:
            if habit.user is not None:
                time_to_start = utc.localize(datetime.now().replace(
                    hour=habit.time_to_start.hour,
                    minute=habit.time_to_start.minute,
                    second=habit.time_to_start.second)
                )
                if utc.localize(datetime.now()) > time_to_start:
                    time_to_start = time_to_start + timedelta(days=1)
                interval = IntervalSchedule.objects.get_or_create(
                    every=habit.interval_value,
                    period='days'
                )
                PeriodicTask.objects.create(
                    name=f'habit_{habit.id}',
                    task=f'send_habit_{habit.pk}_info',
                    interval=IntervalSchedule.objects.get(
                        every=interval[0].every,
                        period=interval[0].period
                    ),
                    start_time=time_to_start,
                    enabled=True
                )
                time_delay = timedelta(
                    minutes=habit.time_for_habit.minute,
                    seconds=habit.time_for_habit.second
                ).total_seconds()
                if habit.reward is None and habit.pleasant_habit is not None:
                    with open(path, 'at') as tasks:
                        function_code = f"""
                        
@shared_task(name='send_habit_{habit.pk}_info')
def send_habit_{habit.pk}():
    habit = habits.get(pk={habit.pk})
    chat_id = habits.get(pk={habit.pk}).user.chat_id
    text1 = f'Ты должен cейчас {{habit.action}} в {{habit.place}}'
    text2 = f'Ура! Ты можешь {{habit.pleasant_habit.action}} в {{habit.pleasant_habit.place}}'
    data_for_request1 = {{'chat_id': chat_id, 'text': text1}}
    data_for_request2 = {{'chat_id': chat_id, 'text': text2}}
    response1 = requests.post(
         f'https://api.telegram.org/bot{{settings.TELEGRAM_BOT_KEY}}/sendMessage',
         data_for_request1)

    time.sleep({time_delay})
    response2 = requests.post(
         f'https://api.telegram.org/bot{{settings.TELEGRAM_BOT_KEY}}/sendMessage',
         data_for_request2)
    final_response = response1.text + ' ' + response2.text
    return final_response
"""
                        tasks.write(function_code)

                elif habit.reward is not None and habit.pleasant_habit is None:
                    with open(path, 'at') as tasks:
                        function_code = f"""
                        
@shared_task(name='send_habit_{habit.pk}_info')
def send_habit_{habit.pk}():
    habit = habits.get(pk={habit.pk})
    chat_id = habits.get(pk={habit.pk}).user.chat_id
    text1 = f'Ты должен сейчас {{habit.action}} в {{habit.place}}'
    text2 = f'Ура! Ты можешь {{habit.reward.action}}'
    data_for_request1 = {{'chat_id': chat_id, 'text': text1}}
    data_for_request2 = {{'chat_id': chat_id, 'text': text2}}
    response1 = requests.post(
         f'https://api.telegram.org/bot{{settings.TELEGRAM_BOT_KEY}}/sendMessage',
         data_for_request1)

    time.sleep({time_delay})
    response2 = requests.post(
         f'https://api.telegram.org/bot{{settings.TELEGRAM_BOT_KEY}}/sendMessage',
         data_for_request2)
    final_response = response1.text + ' ' + response2.text
    return final_response
                    """
                        tasks.write(function_code)

                elif habit.reward is None and habit.pleasant_habit is None:
                    with open(path, 'at') as tasks:
                        function_code = f"""
                        
@shared_task(name='send_habit_{habit.pk}_info')
def send_habit_{habit.pk}():
    habit = habits.get(pk={habit.pk})
    chat_id = habits.get(pk={habit.pk}).user.chat_id
    text1 = f'Ты должен {{habit.action}} в {{habit.time_to_start}} {{habit.place}}'
    data_for_request1 = {{'chat_id': chat_id, 'text': text1}}
    response = requests.post(
               f'https://api.telegram.org/bot{{settings.TELEGRAM_BOT_KEY}}/sendMessage',
                data_for_request1)
    return response.text
                    """
                        tasks.write(function_code)
