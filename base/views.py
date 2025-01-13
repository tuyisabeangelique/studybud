from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Create your views here.


def loginPage(request):
  page = 'login'
  if request.user.is_authenticated:
    return redirect('home')
    
  if request.method == 'POST':
    email = request.POST.get('email').lower()
    password = request.POST.get('password')
    
    try:
      user = User.objects.get(email=email)
    except:
      messages.error(request, "This account does not exist.")
    
    # if user exists, authenticate them. We either get an error or the User's object
    user = authenticate(request, email=email, password=password)
    
    # login method adds a sessionid
    if user is not None:
      login(request, user)
      return redirect('home')
    else :
      messages.error(request, "The username or password is incorrect.")
      
  context = {
    'page': page
  }
  return render(request, 'base/login_register.html', context)

def logoutPage(request):
  logout(request)
  return redirect('home')

def registerPage(request):
  form = MyUserCreationForm()
  if request.method == 'POST':
    form = MyUserCreationForm(request.POST)
    if form.is_valid():
      # save the form but don't commit so we can get the user object
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, "Something went wrong. Try again.")
  
  context = {"form": form}
  return render(request, 'base/login_register.html', context)

def home(request):
  # context must be a dict
  # get all rooms in the db.
  # Note: models by default have id values associated with them

  # q is what was passed into the url. Return rooms that have a topicname that contains the valuen of q. If q == '', that means we will return all rooms
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q) 
    )
  topics = Topic.objects.all()[0:5]
  room_count = rooms.count()
  
  # to be used for recent activity
  room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
  
  context = {"rooms":rooms, "topics":topics, "room_count": room_count, 'room_messages':room_messages}
  return render(request, "base/home.html", context)

def room(request, pk):
  # get a room by a unique value
  room = Room.objects.get(id=pk)
  # get the set of messages related to this room
  room_messages = room.message_set.all()
  # since room has a many-to-many rel. with partic, we can just do .all
  participants = room.participants.all()
  
  if request.method == 'POST':
    message = Message.objects.create(
      user=request.user,
      room=room,
      body=request.POST.get('body')
    )
    room.participants.add(request.user)
    # Stay on the page
    return redirect('room', pk=room.id)
  
  print("request user: ", request.user)
  context = {'room' : room, "room_messages":room_messages, 'participants':participants}
  return render(request, "base/room.html", context)

def user_profile(request, pk):
  user = User.objects.get(id=pk)
  # We must pass in all rooms because we will use the feed component, which takes rooms 
  rooms = user.room_set.all()
  room_messages = user.message_set.all()
  topics = Topic.objects.all()
  context={'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
  return render(request, 'base/profile.html',context)

# If a user is not logged in, prevent them from creating a room. Redirect them to the login page
@login_required(login_url='login')
def create_room(request):
  form = RoomForm()
  topics = Topic.objects.all()
  if request.method == 'POST':
    topic_name = request.POST.get('topic')
    # we might create new topic, or use an existing one. 
    topic, created = Topic.objects.get_or_create(name=topic_name)
    # send into the form the client's post data to save the form into our db, and redirect user
    Room.objects.create(
      host=request.user,
      topic=topic,
      name=request.POST.get('name'),
      description=request.POST.get('description')
    )
    return redirect('home')
    
  context = {"form" : form, "topics":topics}
  return render(request, "base/room_form.html", context)

@login_required(login_url='login')
def update_room(request, pk):
  room = Room.objects.get(id=pk)
  topics = Topic.objects.all()
  
  # we want to get the initial values of room to display in the form 
  form = RoomForm(instance=room)
  
  if request.user != room.host:
    return HttpResponse("Only the room's host can update this room.")
  
  if request.method == 'POST':
    # We will replace the relevant room with the updated form data
    topic_name = request.POST.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)
    room.name = request.POST.get('name')
    room.topic = topic
    room.description = request.POST.get('description')
    room.save()
    return redirect('home')
  
  context = {
    'form': form, 
    "topics":topics,
    "room": room 
  }
  return render(request, 'base/room_form.html', context)
  
@login_required(login_url='login')
def delete_room(request, pk):
  room = Room.objects.get(id=pk)
  # a post method means the user clicked confirm
  
  if request.user != room.host:
    return HttpResponse("Only the room's host can delete this room.")
  
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, "base/delete.html", {'obj': room})

@login_required(login_url='login')
def delete_message(request, pk):
  message = Message.objects.get(id=pk)
  # a post method means the user clicked confirm
  if request.method == 'POST':
    message.delete()
    return redirect('home')
  return render(request, "base/delete.html", {'obj': message})

@login_required(login_url='login')
def update_user(request):
  user = request.user
  form = UserForm(instance=user)
  
  # When we submit the update user form
  if request.method == 'POST':
    form = UserForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
      form.save()
      return redirect('user-profile', pk=user.id)
    
  context = {'form':form}
  return render(request, 'base/update_user.html', context)

def topics_page(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  topics = Topic.objects.filter(name__icontains=q)
  return render(request, 'base/topics.html', {"topics": topics})

def activity_page(request):
  room_messages = Message.objects.all()
  return render(request, 'base/activity.html', {'room_messages': room_messages})