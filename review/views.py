from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def review(request):
    reviews = Review.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('alert')
    else:
        form = ReviewForm()

    context = {
        'form':form,
        'reviews':reviews,
    }

    return render(request, 'review/review.html', context)