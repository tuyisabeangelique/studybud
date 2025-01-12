from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User


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
    fields = [ 'username', 'email']