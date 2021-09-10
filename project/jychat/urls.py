from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('<room_name>/', views.enter_room)
]