from django.urls import path
from . import views

urlpatterns = [
    path('totp/create/', views.TOTPCreateView.as_view(), name='totp-create'),
    path('totp/login/<token>/', views.TOTPVerifyView.as_view(), name='totp-login'),
    path('users/create/', views.UserAPI.as_view(), name='totp-login'),
    path('users/login', views.UserLogin.as_view())
]
