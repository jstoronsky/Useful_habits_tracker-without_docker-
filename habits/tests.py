from rest_framework.test import APITestCase
from rest_framework import status
from habits.models import UsefulHabit, PleasantHabit, Reward
# Create your tests here.


class UsefulHabitTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_create_habit(self):
        """
        тест создания полезной привычки
        """
        data = {
            "place": "Офис",
            "action": "размять спину",
            "interval_value": 1,
            "is_public": True
        }
        response = self.client.post(
            "/habits/create/",
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(),
                         {'id': 7, "user": None, "place": "Офис", "time_to_start": '12:00:00',
                          'time_for_habit': '00:02:00', "action": "размять спину",
                          'pleasant_habit': None,
                          "interval_value": 1, "reward": None,
                          "is_public": True}
                         )
        self.assertTrue(UsefulHabit.objects.all().count() > 0)

    def test_list_habit(self):
        """
        тест вывода списка полезных привычек
        """

        UsefulHabit.objects.create(place="Офис", action="размять спину ещё раз", interval_value=1, is_public=True)
        response = self.client.get(
            '/habits/list/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         [{'id': 8, "user": None, "place": "Офис", "time_to_start": '12:00:00',
                           'time_for_habit': '00:02:00', "action": "размять спину ещё раз",
                           'pleasant_habit': None, 'interval_value': 1, "reward": None,
                           'is_public': True}]
                         )

    def test_update_habit(self):
        """
        тест обновления полезной привычки
        """
        UsefulHabit.objects.create(place="Офис", action="размять спину снова и ещё раз",
                                   interval_value=1, is_public=True)

        data = {
            "place": "Офис",
            "action": "пресс качат, отжумания",
        }

        response = self.client.patch(
            '/habits/update/9/',
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         {'id': 9, "user": None, "place": "Офис", "time_to_start": '12:00:00',
                          'time_for_habit': '00:02:00', "action": "пресс качат, отжумания",
                          'pleasant_habit': None, 'interval_value': 1, "reward": None,
                          'is_public': True}
                         )

        self.client.delete(
            '/habits/delete/9/',
        )

        queryset = UsefulHabit.objects.all()
        self.assertTrue(len(queryset) == 0)

    def test_time_for_habit_validator(self):
        """
        тест валидации поля 'interval_value'
        """
        data = {
            "place": "Офис",
            "action": "размять спину",
            "time_for_habit": "00:03:00",
            "interval_value": 1,
            "is_public": True,
        }
        response = self.client.post(
            "/habits/create/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['This field can not be over 2 minutes']})
        self.assertTrue(UsefulHabit.objects.all().count() == 0)

    def test_habit_or_reward_validator(self):
        """
        тест валидации невозможности заполнить одновременно поля приятной привычки и вознаграждения
        """
        data = {
            "place": "Кухня",
            "action": "вспоминать английские слова",
            "pleasant_habit": {
                "action": "action",
                "place": "place"
            },
            "reward": {
                "action": "вознаграждение"
            },
            "interval_value": 1,
            "is_public": True,
        }

        response = self.client.post(
            "/habits/create/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': [
            'You can not set pleasant habit and reward simultaneously. Choose either first or second'
        ]})

    def tearDown(self):
        UsefulHabit.objects.all().delete()
        PleasantHabit.objects.all().delete()
        Reward.objects.all().delete()
        return super().tearDown()


class PleasantHabitTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_create_habit(self):
        """
        тест создания приятной привычки
        """
        data = {
            "place": "Офис",
            "action": "размять спину",
            "pleasant_habit": {
                "place": "Офис",
                "action": "размять спину",
            },
            "interval_value": 1,
            "is_public": True,
        }
        response = self.client.post(
            "/habits/create/",
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(),
                         {'id': 1, "user": None, "place": "Офис", "time_to_start": '12:00:00',
                          'time_for_habit': '00:02:00', "action": "размять спину",
                          'pleasant_habit': {
                              'id': 1, "place": "Офис",
                              'time_for_habit': '00:02:00', "action": "размять спину"
                          },
                          "interval_value": 1, "reward": None,
                          "is_public": True}
                         )
        self.assertTrue(PleasantHabit.objects.all().count() > 0)

    def test_list_habit(self):
        """
        тест вывода списка полезных привычек с наличием приятной привычки
        """

        pleasant = PleasantHabit.objects.create(place="Офис", action="размять спину ещё раз")
        UsefulHabit.objects.create(place="Офис", action="размять спину ещё раз", interval_value=1, is_public=True,
                                   pleasant_habit=pleasant)
        response = self.client.get(
            '/habits/list/',
            format='json'
        )
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         [{'id': 2, 'pleasant_habit':
                             {
                                 'id': 2, 'place': 'Офис', 'time_for_habit': '00:02:00',
                                 'action': 'размять спину ещё раз'
                             },
                           'reward': None,
                           'place': 'Офис', 'time_to_start': '12:00:00', 'time_for_habit': '00:02:00',
                           'action': 'размять спину ещё раз', 'interval_value': 1, 'is_public': True, 'user': None}]
                         )

    def test_update_habit(self):
        """
        тест обновления приятной привычки
        """
        pleasant = PleasantHabit.objects.create(place="Офис", action="размять спину снова и ещё раз")
        UsefulHabit.objects.create(place="Офис", action="размять спину ещё раз", interval_value=1, is_public=True,
                                   pleasant_habit=pleasant)

        data = {
            "place": "Офис",
            "pleasant_habit": {
                "place": "Офис",
                'time_for_habit': '00:02:00',
                "action": "размять спину"
            },
            "action": "пресс качат, отжумания",
        }

        response = self.client.patch(
            '/habits/update/3/',
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         {'id': 3, 'pleasant_habit':
                             {
                                 'id': 3, 'place': 'Офис', 'time_for_habit': '00:02:00',
                                 'action': 'размять спину'
                             },
                          'reward': None,
                          'place': 'Офис', 'time_to_start': '12:00:00', 'time_for_habit': '00:02:00',
                          'action': 'пресс качат, отжумания', 'interval_value': 1, 'is_public': True, 'user': None}
                         )

        self.client.delete(
            '/habits/delete/3/',
        )

        queryset = PleasantHabit.objects.all()
        self.assertTrue(len(queryset) == 0)

    def tearDown(self):
        UsefulHabit.objects.all().delete()
        PleasantHabit.objects.all().delete()
        return super().tearDown()


class RewardTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_create_reward(self):
        """
        тест создания вознаграждения
        """
        data = {
            "place": "Офис",
            "action": "размять спину",
            "reward": {
                "action": "размять спину",
            },
            "interval_value": 1,
            "is_public": True,
        }
        response = self.client.post(
            "/habits/create/",
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(),
                         {'id': 4, "user": None, "place": "Офис", "time_to_start": '12:00:00',
                          'time_for_habit': '00:02:00', "action": "размять спину",
                          'reward': {
                              'id': 1, "action": "размять спину"
                          },
                          "interval_value": 1, "pleasant_habit": None,
                          "is_public": True}
                         )
        self.assertTrue(Reward.objects.all().count() > 0)

    def test_list_reward(self):
        """
        тест вывода привычек с вознаграждением
        """

        reward = Reward.objects.create(action="размять спину ещё раз")
        UsefulHabit.objects.create(place="Офис", action="размять спину", interval_value=1, is_public=True,
                                   reward=reward)
        response = self.client.get(
            '/habits/list/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         [{'id': 5, "user": None, "place": "Офис", "time_to_start": '12:00:00',
                          'time_for_habit': '00:02:00', "action": "размять спину",
                           'reward': {
                               'id': 2, "action": "размять спину ещё раз"
                           },
                           "interval_value": 1, "pleasant_habit": None,
                           "is_public": True}]
                         )

    def test_update_reward(self):
        """
        тест обновления вознаграждения
        """
        reward = Reward.objects.create(action="размять спину")
        UsefulHabit.objects.create(place="Офис", action="размять спину", interval_value=1, is_public=True,
                                   reward=reward)

        data = {
            "place": "Офис",
            "reward": {
                "action": "размять спину снова и ещё раз"
            },
            "action": "пресс качат, отжумания",
        }

        response = self.client.patch(
            '/habits/update/6/',
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         {'id': 6, 'reward':
                             {
                                 'id': 3,
                                 'action': 'размять спину снова и ещё раз'
                             },
                          'pleasant_habit': None,
                          'place': 'Офис', 'time_to_start': '12:00:00', 'time_for_habit': '00:02:00',
                          'action': 'пресс качат, отжумания', 'interval_value': 1, 'is_public': True, 'user': None}
                         )

        self.client.delete(
            '/habits/delete/6/',
        )

        queryset = Reward.objects.all()
        self.assertTrue(len(queryset) == 0)

    def tearDown(self):
        UsefulHabit.objects.all().delete()
        Reward.objects.all().delete()
        return super().tearDown()
