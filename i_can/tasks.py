from django.utils import timezone

from celery import shared_task

from i_can.models import Habit
from i_can.services import send_telegram_message
from users.models import User


@shared_task
def send_reminder_to_telegram():
    """Отправка напоминания в Телеграм о привычке"""
    now = timezone.now()
    current_time = now.time()
    current_weekday = now.weekday()  # 0-понедельник, 6-воскресенье

    users = User.objects.filter(tg_id__isnull=False)

    for user in users:
        habits = Habit.objects.filter(
            user=user,
            start_time__isnull=False,
            is_reminder_send=False
        )

        for habit in habits:
            # Проверяем день недели (периодичность в днях)
            if habit.periodicity == 0:  # Защита от деления на 0
                continue

            # Проверяем, нужно ли выполнять привычку сегодня
            if current_weekday % habit.periodicity != 0:
                continue

            # Проверяем, наступило ли время для привычки
            if habit.start_time <= current_time:
                # Время пришло - отправляем напоминание
                message = f'Напоминание о привычке:\n{habit.action}\nМесто: {habit.place or "не указано"}\nВремя выполнения: {habit.execution_time} секунд'

                try:
                    send_telegram_message(user.tg_id, message)
                    habit.is_reminder_send = True
                    habit.save()
                    print(f'Отправлено напоминание пользователю {user.email}')
                except Exception as e:
                    print(f'Ошибка отправки пользователю {user.email}: {e}')


@shared_task
def reset_reminder_flags():
    """ Сброс флагов отправки напоминаний каждый день в 00:00 """
    habits = Habit.objects.filter(is_reminder_send=True)
    habits.update(is_reminder_send=False)
    updated_count = len(habits)
    print(f'Сброшены флаги для {updated_count} привычек')