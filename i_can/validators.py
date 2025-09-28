from rest_framework.serializers import ValidationError

from i_can.models import Habit


class HabitFieldsValidator:
    """ Валидатор значений полей объекта Habit """

    def validate_execution_time(self, value):
        """ Проверка времени исполнения привычки """
        if value > 120:
            raise ValidationError('Время исполнения не должно превышать 120 секунд')

    def __call__(self, attrs):
        """ Основная валидация """
        is_pleasant = attrs.get('is_pleasant', False)
        related_habit = attrs.get('related_habit')
        reward = attrs.get('reward')
        periodicity = attrs.get('periodicity', 7)
        start_time = attrs.get('start_time')
        execution_time = attrs.get('execution_time', 120)

        # Проверка времени выполнения
        if execution_time and execution_time > 120:
            raise ValidationError({'execution_time': 'Время исполнения не должно превышать 120 секунд'})

        # Проверка периодичности
        if periodicity and periodicity > 7:
            raise ValidationError({'periodicity': 'Привычка должна выполняться не реже 1 раза в 7 дней'})

        # Валидация для приятных привычек
        if is_pleasant:
            if related_habit:
                raise ValidationError({
                    'related_habit': 'Приятная привычка не может иметь связанную привычку'
                })
            if reward:
                raise ValidationError({
                    'reward': 'Приятная привычка не может иметь вознаграждение'
                })

        # Валидация для полезных привычек
        else:
            # Нельзя одновременно иметь и вознаграждение и связанную привычку
            if related_habit and reward:
                raise ValidationError({
                    'reward': 'Можно указать только вознаграждение ИЛИ связанную привычку',
                    'related_habit': 'Можно указать только вознаграждение ИЛИ связанную привычку'
                })

            # Должны быть заполнены обязательные поля
            if not start_time:
                raise ValidationError({
                    'start_time': 'Для полезной привычки должно быть указано время начала'
                })

            # Должно быть либо вознаграждение, либо связанная привычка
            if not reward and not related_habit:
                raise ValidationError({
                    'reward': 'Для полезной привычки должно быть указано вознаграждение ИЛИ связанная привычка',
                    'related_habit': 'Для полезной привычки должно быть указано вознаграждение ИЛИ связанная привычка'
                })

            # Если указана связанная привычка, она должна быть приятной
            if related_habit and not related_habit.is_pleasant:
                raise ValidationError({
                    'related_habit': 'Связанная привычка должна быть приятной'
                })



