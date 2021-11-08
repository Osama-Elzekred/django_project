from typing import List
from django import http
from django.shortcuts import redirect, render , get_object_or_404
from django.http import HttpResponse ,HttpResponseRedirect
from django.urls import reverse , reverse_lazy
from .models import Comment, Post
from .forms import CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import (
     ListView ,
     DetailView,
     CreateView,
     UpdateView,
     DeleteView,
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
        post.dislikes.remove(request.user)
        liked= True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   #redirect to the same page
  else  : 
      return HttpResponseRedirect(reverse('login'))  

def DisLikeView(request,pk):
  if request.user.is_authenticated:
        
    post = get_object_or_404(Post, pk=pk)
    disliked=False
    if post.dislikes.filter(id=request.user.id).exists() :
        post.dislikes.remove(request.user)
        disliked=False
    else:
        post.dislikes.add(request.user)
        disliked= True
        post.likes.remove(request.user)

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
    paginate_by= 5
    
    # To display the comments
    def get_context_data(self, *args,**kwargs) :
      context = super(PostListView,self).get_context_data( *args,**kwargs)
      post_comments = Comment.objects.all()
      context['comments']=post_comments
      return context

class UserPostListView(ListView):
    model = Post 
    template_name = 'blog/user_posts.html'
    context_object_name='posts'  
    paginate_by= 5

    def get_queryset(self) : 
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# Detail view dosent allow POST by default
class PostDetailView(DetailView):
    model = Post 
    http_method_names = ['get', 'post']	
    #  defualt looking for :  <app>/<model>_<viewtype>.html
    #             which is : blog/post_detail.html 

    form = CommentForm()
    def post(self, request, *args, **kwargs):
        form= CommentForm(request.POST)
        if request.user.is_authenticated :
          if form.is_valid():
              post=self.get_object()
              form.instance.author=request.user
              form.instance.post=post
              form.save()
  
              return redirect(reverse('post-detail',kwargs={'pk':post.pk}))
        return HttpResponseRedirect(reverse('login'))  


    
    def get_context_data(self, *args,**kwargs) :
      context = super(PostDetailView,self).get_context_data( *args,**kwargs)
      post_comments = Comment.objects.filter(post=self.object.id)
      context['comments']=post_comments
      context['form'] = self.form
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
    fields=['title','content','image']

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

class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Comment
    template_name='blog/comment_delete.html'
    
    def get_success_url(self):
        pk=self.kwargs['post_pk'] #  post_pk in the url  
        return reverse_lazy('post-detail',kwargs={'pk':pk})

    def test_func(self):
        comment=self.get_object()
        if self.request.user == comment.author:
            return True
        return False

def About(request):
    return render(request, 'blog/about.html', {'title': 'about'})
