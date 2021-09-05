from django import forms
from django.contrib.auth import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.fields import ChoiceField


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