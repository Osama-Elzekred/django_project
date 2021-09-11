from typing import List
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import (
     ListView ,
     DetailView,
     CreateView,
     UpdateView,
     DeleteView
)


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post 

    template_name = 'blog/home.html'

    #  defualt looking for :  <app>/<model>_<viewtype>.html
    #             which is : blog/post_list.html 

    context_object_name='posts'  
    # defualt name for the objects is 'object'
    
    ordering= ['-date_posted']


class PostDetailView(DetailView):
    model = Post 
    #  defualt looking for :  <app>/<model>_<viewtype>.html
    #             which is : blog/post_detail.html 

class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post 
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin ,UserPassesTestMixin,UpdateView):
 # login and userpass  must be in the left of the class prameters 
    model = Post 
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False
   

def About(request):
    return render(request, 'blog/about.html', {'title': 'about'})
