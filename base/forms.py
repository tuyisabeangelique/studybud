from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm 

class MyUserCreationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['name', 'username', 'email', 'password1', 'password2']


# form for the Room model
class RoomForm(ModelForm):
  class Meta:
    model = Room
    # We will have fields for all values in our model. 
    fields = '__all__'
    exclude = ['host', 'participants']
    
class UserForm(ModelForm):
  class Meta:
    model = User
    fields = [ 'avatar', 'name', 'username', 'email', 'bio']