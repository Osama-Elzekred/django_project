from django.urls import path
from . import views

urlpatterns=[
  path('',views.home , name='Home-blog'),
  path('about/',views.About, name='About-blog'),

  ]