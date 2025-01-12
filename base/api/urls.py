from django.urls import path 
from . import views

urlpatterns = [
  path('', views.getRoutes),
  path('rooms/', views.get_rooms),
  path('rooms/<str:pk>/', views.get_room),
]