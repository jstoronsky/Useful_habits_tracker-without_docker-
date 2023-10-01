from celery import shared_task
import requests
from django.conf import settings
import time
from habits.models import UsefulHabit

habits = UsefulHabit.objects.all()

                        
@shared_task(name='send_habit_43_info')
def send_habit_43():
    habit = habits.get(pk=43)
    chat_id = habits.get(pk=43).user.chat_id
    text1 = f'Ты должен сейчас {habit.action} в {habit.place}'
    text2 = f'Ура! Ты можешь {habit.reward.action}'
    data_for_request1 = {'chat_id': chat_id, 'text': text1}
    data_for_request2 = {'chat_id': chat_id, 'text': text2}
    response1 = requests.post(
         f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_KEY}/sendMessage',
         data_for_request1)

    time.sleep(120.0)
    response2 = requests.post(
         f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_KEY}/sendMessage',
         data_for_request2)
    final_response = response1.text + ' ' + response2.text
    return final_response
                    