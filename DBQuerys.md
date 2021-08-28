Post.objects.first.content => 'Frist post Content ever !'

post =Post.objects.filter(author_id=1) => <QuerySet [<Post: blog 1>, <Post: Blog 2>]>
user = post.author => <User: osama>

user.post_set.all() => <QuerySet [<Post: blog 1>, <Post: Blog 2>]>

user.post_set.create(title=' blog 3 ',content='Third post content ! ') => <Post: blog 3 >

Post.objects.all() => <QuerySet [<Post: blog 1>, <Post: Blog 2>, <Post: blog 3 >]>
