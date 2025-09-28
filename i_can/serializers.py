from rest_framework import serializers

from i_can.models import Habit
from i_can.validators import HabitFieldsValidator


class HabitSerializer(serializers.ModelSerializer):
    """ Сериализатор для объектов привычек """
    model = Habit
    fields = '__all__'

    def validate(self, attrs):
        """Валидация на уровне сериализатора"""
        validator = HabitFieldsValidator()
        validator(attrs)
        return attrs


class PublicHabitSerializer(serializers.ModelSerializer):
    """ Сериализатор для публичных привычек """
    class Meta:
        model = Habit
        fields = ("action", "is_pleasant", "execution_time")
