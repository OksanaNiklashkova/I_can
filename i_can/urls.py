from django.urls import path

from .apps import ICanConfig
from . import views

app_name = ICanConfig.name

urlpatterns = [
    path('habit_create/', views.HabitCreateAPIView.as_view(), name='habit_create'),
    path('public/', views.PublicHabitListAPIView.as_view(), name='public'),
    path('', views.HabitListAPIView.as_view(), name='habits'),
    path('habit/<int:pk>/', views.HabitRetrieveAPIView.as_view(), name='habit'),
    path('habit_update/<int:pk>/', views.HabitUpdateAPIView.as_view(), name='habit_update'),
    path('habit_delete/<int:pk>/', views.HabitDestroyAPIView.as_view(), name='habit_delete'),

]