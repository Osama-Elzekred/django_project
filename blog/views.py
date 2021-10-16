from typing import List
from django import http
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse ,HttpResponseRedirect
from django.urls import reverse
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import (
     ListView ,
     DetailView,
     CreateView,
     UpdateView,
     DeleteView
)



# def home(request): 
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)
 
def LikeView(request,pk):
  if request.user.is_authenticated:
        
    post = get_object_or_404(Post, pk=pk)
    liked=False
    if post.likes.filter(id=request.user.id).exists() :
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked= True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   #redirect to the same page
  else  : 
      return HttpResponseRedirect(reverse('login'))  



class PostListView(ListView):
    model = Post 

    template_name = 'blog/home.html'

    #  defualt looking for :  <app>/<model>_<viewtype>.html
    #             which is : blog/post_list.html 

    context_object_name='posts'  
    ordering= ['-date_posted']
    paginate_by= 4 


class UserPostListView(ListView):
    model = Post 
    template_name = 'blog/user_posts.html'
    context_object_name='posts'  
    paginate_by= 5

    def get_queryset(self) : 
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post 
    #  defualt looking for :  <app>/<model>_<viewtype>.html
    #             which is : blog/post_detail.html 
    def get_context_data(self, *args,**kwargs) :
      context = super(PostDetailView,self).get_context_data( *args,**kwargs)
      context['posts']=Post.objects.all()
      return context

class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post 
    fields=['title','content','image']

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
