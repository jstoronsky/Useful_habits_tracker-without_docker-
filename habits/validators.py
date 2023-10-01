from datetime import timedelta

from rest_framework.serializers import ValidationError


class HabitOrRewardValidator:
    """
    Валидация на невозможность одновременного наличия у полезной привычки приятной привычки и вознаграждения
    """
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        field1 = dict(value).get(self.field1)
        field2 = dict(value).get(self.field2)
        if field1 is not None and field2 is not None:
            raise ValidationError('You can not set pleasant habit and reward simultaneously. Choose either '
                                  'first or second')


class TimeForHabitValidator:
    """
    Валидация на невозможность установить время на привычку больше чем две минуты
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        field = dict(value).get(self.field)
        if field is not None:
            if timedelta(hours=field.hour, minutes=field.minute,
                         seconds=field.second) > timedelta(seconds=120):
                raise ValidationError('This field can not be over 2 minutes')
