from django.shortcuts import render
from .models import Entry
# Create your views here.

def blog(request):
    entries = Entry.objects.all()

    context = {
        'entries':entries,
    }

    return render(request, 'blog/blog.html', context)