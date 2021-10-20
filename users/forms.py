from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from django.forms.fields import ChoiceField
from .models import Profile


GENDER= (
  ('Male','Male'),
  ('Female','Female'),
  ('civil engineer','civil engineer'),
)
class UserRegisterForm(UserCreationForm):
  email = forms.EmailField() 
  gender = forms.ChoiceField(choices=GENDER)
  class Meta :
    model = User
    fields = ['username','email','gender','password1','password2']


class UserUpdateForm(forms.ModelForm):
  email = forms.EmailField() 
  class Meta :
    model = User
    fields = ['username','email']
  
class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model=Profile
    fields=['image','bio']