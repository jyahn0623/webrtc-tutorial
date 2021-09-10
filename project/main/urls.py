from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('<str:room_name>/', views.room)
]
