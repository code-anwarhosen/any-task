from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo, name='todo'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    path('task_complete/<str:slug>/', views.task_complete, name='task_complete'),
    path('edit/', views.edit, name='edit'),
    path('delete/<str:slug>/', views.delete, name='delete'),
]
