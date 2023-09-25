from rest_framework.serializers import ValidationError


class HabitOrRewardValidator:

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        field1 = dict(value).get(self.field1)
        field2 = dict(value).get(self.field2)
        if field1 is not None and field2 is not None:
            raise ValidationError('You can not set pleasant habit and reward simultaneously. Choose either '
                                  'first or second')
