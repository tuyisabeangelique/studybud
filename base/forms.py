from django.forms import ModelForm
from .models import Room

# form for the Room model
class RoomForm(ModelForm):
  class Meta:
    model = Room
    # We will have fields for all values in our model. 
    fields = '__all__'
    exclude = ['host', 'participants']