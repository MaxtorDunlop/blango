from django.shortcuts import render
from django.utils import timezone
from blog.models import Post
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from blog.forms import CommentForm

def index(request):

  # If we don’t need all the data for a particular model, we can use 
  # the QuerySet methods defer() and only() to control which columns
  # are retrieved and in-turn converted to Python. These methods are 
  # basically the opposite of each other: defer() takes one or more
  # string arguments which are columns to not load data for. On the
  # contrary, only() takes the columns to only load data for. That’s
  # not to say that the unloaded fields aren’t accessible though. 
  # If you try to access one of them in Python, Django makes a database
  # query to fetch that field.
  #posts = (
  #  Post.objects.filter(published_at__lte=timezone.now())
  #  .select_related("author")
  #  .only("title", "summary", "content", "author", "published_at", "slug")
#)
  #posts = (
  #  Post.objects.filter(published_at__lte=timezone.now())
  #  .select_related("author")
  #  .defer("created_at", "modified_at")
#)
  posts = Post.objects.filter(published_at__lte=timezone.now()).select_related("author")
  return render(request, "blog/index.html", {"posts":posts})

def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug)
  if request.user.is_active:
    if request.method == "POST":
      comment_form = CommentForm(request.POST)

      if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.content_object = post
        comment.creator = request.user
        comment.save()
        return redirect(request.path_info)
    else:
      comment_form = CommentForm()
  else:
    comment_form = None
  return render(
    request, "blog/post-detail.html", {"post": post, "comment_form": comment_form}
  )

def get_ip(request):
  from django.http import HttpResponse
  return HttpResponse(request.META['REMOTE_ADDR'])
