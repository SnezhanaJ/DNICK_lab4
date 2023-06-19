from django.shortcuts import render, redirect
from .models import Post, UserProfile
from .forms import PostForm, BlockForm


# Create your views here.
def posts(request):
    queryset = Post.objects.all()
    context = {"posts": queryset}
    return render(request, "index.html", context=context)


def profiles(request):
    profile_details = UserProfile.objects.get(user=request.user)
    profile_posts = Post.objects.all()
    context = {"user": profile_details, "posts": profile_posts}
    return render(request, "profile.html", context=context)


def add(request):
    if request.method == "POST":
        form_data = PostForm(data=request.POST, files=request.FILES)

        if form_data.is_valid():
            post = form_data.save(commit=False)
            post.user = UserProfile.objects.get(user=request.user)
            post.save()

            return redirect("posts")

    return render(request, "add.html", {"form": PostForm})


def blocked(request):
    if request.method == "POST":
        form_data = BlockForm(data=request.POST, files=request.FILES)

        if form_data.is_valid():
            block = form_data.save(commit=False)
            block.blocker = UserProfile.objects.get(user=request.user)
            block.save()

            return redirect("blocked")
        return render(request, "blocked.html", {"form": BlockForm})
