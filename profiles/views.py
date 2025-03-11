from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from forum.models import Post, Comment, Community, PostView, CommunityView, CommunityGroup

from itertools import chain
from operator import attrgetter
# Create your views here.

def my_profil(request):
    return redirect('profile', request.user.username)

def profile(request, username):
    user_model = get_user_model()
    user = get_object_or_404(user_model, username=username)

    # Отримуємо всі пости та коментарі
    posts = Post.objects.filter(created_by=user)
    comments = Comment.objects.filter(user=user)
    
    # Об’єднуємо та сортуємо за атрибутом created_at
    actions = sorted(chain(posts, comments), key=attrgetter('created_at'), reverse=True)

    context = {
        'user': user,
        'actions': actions,
    }
    return render(request, 'profiles/profile.html', context)

def posted(request, username):
    user_model = get_user_model()
    user = get_object_or_404(user_model, username=username)

    posts = Post.objects.filter(created_by=user)

    context = {
        'posts':posts,
    }

    return render(request, 'profiles/posts.html', context)

def commented(request, username):
    user_model = get_user_model()
    user = get_object_or_404(user_model, username=username)

    comments = Comment.objects.filter(user=user)

    context = {
        'comments':comments,
    }

    return render(request, 'profiles/comments.html', context)

def liked(request, username):
    user_model = get_user_model()
    user = get_object_or_404(user_model, username=username)

    posts = Post.objects.filter(likes__user=user)

    context = {
        'posts':posts,
    }

    return render(request, 'profiles/posts.html', context)

def history(request):
    if not request.user.is_authenticated:
        return redirect('login')

    history = PostView.objects.filter(user=request.user)

    context = {
        'history':history,
    }

    return render(request, 'profiles/history.html', context)

def community_group(request, username, slug):
    # group = CommunityGroup.objects.filter(creator__username=username, slug=slug)
    group = get_object_or_404(CommunityGroup, slug=slug)
    communities = Community.objects.filter(group_item__group=group)
    posts = Post.objects.filter(community__in=communities).order_by('-created_at')

    context = {
        'group': group,
        'communities': communities,
        'posts': posts,
    }

    return render(request, 'profiles/community_group.html', context)