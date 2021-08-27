from django.shortcuts import render
from django.http import HttpResponse

posts = [

    {
        'author': 'OsamaElzekred',
        'title': 'Blog post 1 ',
        'content': 'Frist post content',
        'date_posted': '2021/8/17'
    },
    {
        'author': 'SaraElzekred',
        'title': 'Blog post 2 ',
        'content': 'second post content',
        'date_posted': '2021/8/18'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def About(request):
    return render(request, 'blog/about.html', {'title': 'about'})
