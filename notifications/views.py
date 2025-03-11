from django.shortcuts import render
from .models import Notification
from .forms import NotificationSortForm

# Create your views here.
def notifications(request):
    sort_form = NotificationSortForm()

    sort_by = request.GET.get('sort_by', 'all')
    sort_form = NotificationSortForm(initial={'sort_by': sort_by})

    if sort_by == 'all':
        notifications = Notification.objects.filter(user=request.user)
    elif sort_by == 'unreadet':
        notifications = Notification.objects.filter(user=request.user, is_read=False)    
    elif sort_by == 'readet':
        notifications = Notification.objects.filter(user=request.user, is_read=True)
    else:
        notifications = Notification.objects.filter(user=request.user)




    context = {
        'notifications': notifications,
        'sort_form': sort_form,
    }

    return render(request, 'notifications/inbox.html', context)