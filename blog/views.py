from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry, Like
# Create your views here.

def blog(request):
    entries = Entry.objects.all()

    context = {
        'entries':entries,
    }

    return render(request, 'blog/blog.html', context)

def entry_like(request, pk):
    liked = Like.objects.filter(entry=entry, user=request.user).first()
    entry = get_object_or_404(Entry, pk=pk)
    if request.user.is_authenticated:

        if liked:
            liked.delete()
        else:
            Like.objects.create(entry=entry, user=request.user)
        return redirect('blog')
    else:
        return redirect('login')