from blog.models import Post

def added_models_ToBase(request):
    return {
        'posts':Post.objects.all()
    }