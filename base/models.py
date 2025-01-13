from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  name = models.CharField(max_length=200, null=True)
  email = models.EmailField(unique=True, null=True)
  bio = models.TextField(null=True)
  avatar = models.ImageField(null=True, default="avatar.png")
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

class Topic(models.Model):
  # A room is associated with a topic like "Java", "Python", "Web Dev"
  
  # A topic can have multiple rooms, but a room can only have one topic. When we delete a topic, we set the room to null (done below in the Room model)
  name = models.CharField(max_length=200)
  
  def __str__(self):
    return self.name

class Room(models.Model):
  # the host is the user who created the room. setting null = True from description means that the db can make it blank if it's is null. Participants will store all users active in a room. Updated sets whenever the model is updated, bc of the keywork auto_now. auto_now_add only takes a timestamp of when we create it. Name is the title like "Let's learn JavaScript"
  
  host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
  name = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  participants = models.ManyToManyField(User, related_name='participants', blank=True)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)
  
  # makes sure that most recently updated  Room is ordered first, and then most recently created
  class Meta:
    ordering = ['-updated', '-created']
  
  def __str__(self):
    return self.name
  
class Message(models.Model):
  # Each room has a message sent by a user. Each message is connected to a room. When Room is deleted, we cascade delete all messages in that room. When User is deleted, we cascade delete all their messages.
  
  # Many-to-one relationship: A user can have many messages. A message can only have one user
  
  # django has a user model we will use.
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  body = models.TextField()
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    ordering = ['-updated', '-created']
    
  def __str__(self):
    # return first 50 chars of message
    return self.body[0:50]
    