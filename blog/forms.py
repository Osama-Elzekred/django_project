from django import forms
from django.forms import fields
from .models import Comment

class CommentForm (forms.ModelForm):
  body = forms.CharField(
    label='',
    widget=forms.Textarea(attrs={'rows':'2','placeholder':'Say something...','class':'md-textarea form-control'})
    )
  class Meta :
    model = Comment
    fields= ['body']