from django.urls import path
from . import views

urlpatterns = [
  # primary key = pk :: id. we are specifying that pk is a string. 
  path('login/', views.loginPage, name="login"),
  path('logout/', views.logoutPage, name="logout"),
  path('register/', views.registerPage, name="register"),
  path('', views.home, name="home"),
  path('room/<str:pk>', views.room, name="room"), 
  path('profile/<str:pk>', views.user_profile, name="user-profile"), 
  path('create-room/', views.create_room, name="create-room"),
  path('update-room/<str:pk>', views.update_room, name="update-room"),
  path('delete-room/<str:pk>', views.delete_room, name="delete-room"),
  path('delete-message/<str:pk>', views.delete_message, name="delete-message"),
  path('update-user/', views.update_user, name="update-user"),
  path('topics/', views.topics_page, name="topics"),
  path('activity/', views.activity_page, name="activity"),
  
]
